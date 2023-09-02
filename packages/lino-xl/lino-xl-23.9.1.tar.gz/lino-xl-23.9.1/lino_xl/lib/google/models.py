# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import logging
from django.conf import settings
from django.db import models
from django.utils import timezone

try:
    from googleapiclient.errors import HttpError
except:
    HttpError = Exception
from typing import NamedTuple

from etgen.html2rst import RstTable
from etgen.html import E
from lino.mixins import Modified
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.users.models import User
from lino_xl.lib.cal.models import BaseSubscription
from lino.api import rt, dd, _
from lino.core.roles import SiteAdmin, SiteStaff

from .utils import make_api_call, get_credentials, build, update_creds
from .choicelists import AccessRoles, google_status
from .mixins import GoogleContactSynchronized

logger = logging.getLogger("lino_xl.lib.google.models")


class CalendarSubscription(BaseSubscription, Modified):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "CalendarSubscription")

    primary = dd.BooleanField(default=False)
    access_role = AccessRoles.field(default='owner')
    sync_token = dd.CharField(max_length=200, blank=True, null=True)
    """Used to retrieve only the changed entries from the remote server."""
    page_token = dd.CharField(max_length=200, blank=True, null=True)


dd.inject_field("users.User", "calendar_sync_token", dd.CharField(max_length=200, blank=True, null=True))
dd.inject_field("users.User", "calendar_page_token", dd.CharField(max_length=200, blank=True, null=True))


class DeletedEntry(dd.Model):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "DeletedEntry")

    calendar = dd.BooleanField(default=False)
    user = dd.ForeignKey('users.User', null=False, blank=False)
    event_id = dd.CharField(max_length=200, blank=True, null=True)
    calendar_id = dd.CharField(max_length=200)


class Contact(UserAuthored, GoogleContactSynchronized, Modified):
    allow_cascaded_delete = ["contact"]
    quick_search_fields = "contact__name"

    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "Contact")

    contact = dd.ForeignKey(dd.plugins.google.contacts_model)


class DeletedContact(UserAuthored):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "DeletedContact")

    contact_id = dd.CharField(max_length=200)


class ContactSyncToken(UserAuthored, Modified):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "ContactSyncToken")
        unique_together = ['user']

    sync_token = dd.CharField(max_length=300, null=True, blank=True)
    page_token = dd.CharField(max_length=300, null=True, blank=True)


def get_user_country(self):
    if self.partner is None or self.partner.country is None:
        return None
    return self.partner.country


User.get_country = get_user_country



class FailedEntries(NamedTuple):
    calendars = []
    events = []
    contacts = []


class Stats(object):
    calendars__in_insert = 0
    calendars__in_update = 0
    events__in_insert = 0
    events__in_update = 0
    contacts__in_insert = 0
    contacts__in_update = 0
    calendars_deleted__in = 0
    events_deleted__in = 0
    contacts_deleted__in = 0
    calendars__out_insert = 0
    calendars__out_update = 0
    events__out_insert = 0
    events__out_update = 0
    contacts__out_insert = 0
    contacts__out_update = 0
    calendars_deleted__out = 0
    events_deleted__out = 0
    contacts_deleted__out = 0

    @property
    def calendars(self):
        return (self.calendars_deleted__out + self.calendars_deleted__in + self.calendars__out_update
                + self.calendars__out_insert + self.calendars__in_insert + self.calendars__in_update)

    @property
    def events(self):
        return (self.events_deleted__out + self.events_deleted__in + self.events__out_update
                + self.events__out_insert + self.events__in_insert + self.events__in_update)

    @property
    def contacts(self):
        return (self.contacts_deleted__out + self.contacts_deleted__in + self.contacts__out_update
                + self.contacts__out_insert + self.contacts__in_insert + self.contacts__in_update)

    def to_rst(self):
        return RstTable(["", "Calendars", "Events", "Contacts"]).to_rst(
            [
                ["Inserted (inward)", self.calendars__in_insert, self.events__in_insert, self.contacts__in_insert],
                ["Inserted (outward)", self.calendars__out_insert, self.events__out_insert, self.contacts__out_insert],
                ["Updated (inward)", self.calendars__in_update, self.events__in_update, self.contacts__in_update],
                ["Updated (outward)", self.calendars__out_update, self.events__out_update, self.contacts__out_update],
                ["Deleted (inward)", self.calendars_deleted__in, self.events_deleted__in, self.contacts_deleted__in],
                ["Deleted (outward)", self.calendars_deleted__out, self.events_deleted__out, self.contacts_deleted__out],
                ["", "", "", ""],
                ["Total modified", self.calendars, self.events, self.contacts]
            ]
        )

    def to_html(self):
        return E.table(
            E.thead(E.tr(E.th(), E.th("Calendars"), E.th("Events"), E.th("Contacts"))),
            E.tbody(
                E.tr(E.td("Inserted (inward)"), E.td(self.calendars__in_insert), E.td(self.events__in_insert), E.td(self.contacts__in_insert)),
                E.tr(E.td("Inserted (outward)"), E.td(self.calendars__out_insert), E.td(self.events__out_insert), E.td(self.contacts__out_insert)),
                E.tr(E.td("Updated (inward)"), E.td(self.calendars__in_update), E.td(self.events__in_update), E.td(self.contacts__in_update)),
                E.tr(E.td("Updated (outward)"), E.td(self.calendars__out_update), E.td(self.events__out_update), E.td(self.contacts__out_update)),
                E.tr(E.td("Deleted (inward)"), E.td(self.calendars_deleted__in), E.td(self.events_deleted__in), E.td(self.contacts_deleted__in)),
                E.tr(E.td("Deleted (outward)"), E.td(self.calendars_deleted__out), E.td(self.events_deleted__out), E.td(self.contacts_deleted__out)),
                E.tr(E.td(), E.td(), E.td(), E.td()),
                E.tr(E.td("Total modified"), E.td(self.calendars), E.td(self.events), E.td(self.contacts))
            )
        )


class Synchronizer:

    logging_frequency = None

    _failed_entries = None
    _stats = None
    failed_entries = None
    stats = None
    user = None
    credentials = None

    def __init__(self, user=None, logging_frequency=None):
        if user is not None:
            self.setup(user, logging_frequency)

    def setup(self, user, logging_frequency=None):
        self.clear()
        self.user = user
        self.stats = Stats()
        self.failed_entries = FailedEntries()
        self.credentials = get_credentials(user)
        self.logging_frequency = (
            logging_frequency if logging_frequency is not None
            else dd.plugins.google.sync_logging_frequency)

    def has_scope_contacts(self):
        return dd.plugins.google.has_scope('contact', self.user)

    def has_scope_calendar(self):
        return dd.plugins.google.has_scope('calendar', self.user)

    def pull_events(self, resource, sub, room):
        Event = rt.models.cal.Event

        def sync10():
            try:
                events = make_api_call(
                    lambda: resource.events().list(
                        calendarId=sub.calendar.google_id, maxResults=10,
                        syncToken=sub.sync_token, pageToken=sub.page_token)
                )
                sub.sync_token = events.get('nextSyncToken') or sub.sync_token
            except HttpError:
                return

            if items := events['items']:
                for item in items:
                    try:
                        Event.insert_or_update_google_event(item, room, synchronizer=self)
                        if (evs := self.stats.events) % self.logging_frequency == 0:
                            logger.info(f"google.Synchronizer ({self.user}): synchronized {evs} events so far.")
                    except Exception as e:
                        logger.exception(e)
                        logger.error(f"failed cal.Event item: {item}")
                        return

            if next_page_token := events.get('nextPageToken'):
                sub.page_token = next_page_token
                sync10()
            else:
                sub.page_token = None

        sync10()
        sub.full_clean()
        sub.save()

    def sync_calendar(self):
        logger.info(f"Synchronizing google calendar for user: {self.user}")
        gcal = build("calendar", "v3", credentials=self.credentials)

        Calendar = rt.models.cal.Calendar
        CalendarSubscription = rt.models.google.CalendarSubscription
        Event = rt.models.cal.Event

        # Outward sync

        if not settings.SITE.is_demo_site:
            cal_res = gcal.calendars()
            ers = gcal.events()

            Calendar.sync_deleted_records(self, cal_res)
            Event.sync_deleted_records(self, ers)

            synched_cals = []

            for c in (qs := Calendar.get_outward_insert_update_queryset(self.user)):
                try:
                    c.insert_or_update_into_google(cal_res, synchronizer=self)
                    synched_cals.append(c.pk)
                except HttpError:
                    continue
                if (cs := self.stats.calendars) % self.logging_frequency == 0:
                    logger.info(f"google.Synchronizer ({self.user}): synchronized {cs} calendars so far.")

            if (qs := qs.exclude(pk__in=synched_cals)).count():
                self.failed_entries.calendars.append(qs)

            synched_events = []
            for e in (qs := Event.get_outward_insert_update_queryset(self.user)):
                try:
                    e.insert_or_update_into_google(ers, synchronizer=self)
                    synched_events.append(e.pk)
                except HttpError:
                    continue

                if (evs := self.stats.events) % self.logging_frequency == 0:
                    logger.info(f"google.Synchronizer ({self.user}): synchronized {evs} events so far.")

            if (qs := qs.exclude(pk__in=synched_events)).count():
                self.failed_entries.events.append(qs)

        # Inward sync

        def sync10():
            try:
                cals = make_api_call(
                    lambda: gcal.calendarList().list(
                        maxResults=10, syncToken=self.user.calendar_sync_token, showDeleted=True,
                        showHidden=True, pageToken=self.user.calendar_page_token
                    )
                )
            except HttpError:
                return

            for cal in cals.get("items", []):
                if cal.get("deleted", False):
                    Calendar.delete_google_calendar(cal)
                    self.stats.calendars_deleted__in += 1
                    if (cs := self.stats.calendars) % self.logging_frequency == 0:
                        logger.info(f"google.Synchronizer ({self.user}): synchronized {cs} calendars so far.")
                    continue
                try:
                    calendar, room = Calendar.insert_or_update_google_calendar(cal, synchronizer=self)
                except Exception as e:
                    logger.exception(e)
                    logger.error(f"failed calendar item: {cal}")
                    return

                if (cs := self.stats.calendars) % self.logging_frequency == 0:
                    logger.info(f"google.Synchronizer ({self.user}): synchronized {cs} calendars so far.")

                try:
                    subscription = CalendarSubscription.objects.get(user=self.user, calendar=calendar)
                except CalendarSubscription.DoesNotExist:
                    subscription = CalendarSubscription(user=self.user, calendar=calendar)
                    ar = CalendarSubscription.get_default_table().request(user=self.user)
                    subscription.full_clean()
                    subscription.save_new_instance(ar)
                subscription.primary = cal.get("primary", False)
                subscription.access_role = cal.get("accessRole", "reader")
                subscription.full_clean()
                subscription.save()

                self.pull_events(gcal, subscription, room)

            if next_page_token := cals.get('nextPageToken'):
                self.user.calendar_page_token = next_page_token
                sync10()
            else:
                self.user.calendar_page_token = None
                self.user.calendar_sync_token = cals.get('nextSyncToken')

        sync10()
        self.user.full_clean()
        self.user.save()

        gcal.close()

    def sync_contacts(self):
        logger.info(f"Synchronizing google contacts for user: {self.user}")
        Contact = rt.models.google.Contact

        token, __ = rt.models.google.ContactSyncToken.objects.get_or_create(user=self.user)
        people = build("people", "v1", credentials=self.credentials).people()

        if not settings.SITE.is_demo_site:
            Contact.sync_deleted_records(self, people)
            synched = []
            for c in (qs := Contact.get_outward_insert_update_queryset(self.user)):
                try:
                    c.insert_or_update_into_google(people, synchronizer=self)
                    synched.append(c.pk)
                    if (cns := self.stats.contacts) % self.logging_frequency == 0:
                        logger.info(f"google.Synchronizer ({self.user}): synchronized {cns} contacts so far.")
                except HttpError:
                    break

            if (qs := qs.exclude(pk__in=synched)).count():
                self.failed_entries.contacts.append(qs)

        def sync10():
            try:
                resp = make_api_call(lambda: people.connections().list(
                    resourceName="people/me",
                    personFields=Contact.person_fields,
                    pageToken=token.page_token,
                    syncToken=token.sync_token,
                    pageSize=10,
                    requestSyncToken=True
                ))
            except HttpError:
                return

            if "connections" not in resp:
                token.page_token = None
                token.sync_token = resp["nextSyncToken"]
                return resp

            for item in resp["connections"]:
                if (ks := len(item.keys())) == 2:
                    Contact.delete_google_contact(item, synchronizer=self)
                    if (cns := self.stats.contacts) % self.logging_frequency == 0:
                        logger.info(f"google.Synchronizer ({self.user}): synchronized {cns} contacts so far.")
                    continue
                assert ks > 2  # probably not needed, keep just to see in case something breaks
                try:
                    Contact.insert_or_update_google_contact(item, synchronizer=self)
                except Exception as e:
                    logger.exception(e)
                    logger.error(f"failed contact item: {item}")
                    return

                if (cns := self.stats.contacts) % self.logging_frequency == 0:
                    logger.info(f"google.Synchronizer ({self.user}): synchronized {cns} contacts so far.")

            if pageToken := resp.get("nextPageToken"):
                token.page_token = pageToken
                sync10()
            else:
                token.page_token = None
                token.sync_token = resp["nextSyncToken"]

        sync10()

        token.full_clean()
        token.save()
        people.close()

    def __call__(self, cal_only=False, contacts_only=False):
        if self.user is None:
            raise Exception("Invalid google.Synchronizer instance, does not have a user scope, please call setup")
        try:
            if not contacts_only:
                if self.has_scope_calendar():
                    self.sync_calendar()
                else:
                    logger.info(f"google.Synchronizer({self.user}): does not have the necessary scopes to sync Google calendar")

            if not cal_only:
                if self.has_scope_contacts():
                    self.sync_contacts()
                else:
                    logger.info(f"google.Synchronizer({self.user}): does not have the necessary scopes to sync Google contacts")

            # update the modification timestamp of the sync tokens
            self.user.full_clean()
            self.user.save()
            rt.models.google.CalendarSubscription.objects.filter(user=self.user).update(modified=timezone.now())
            rt.models.google.ContactSyncToken.objects.filter(user=self.user).update(modified=timezone.now())

            # update the modification timestamp of the failed entries
            for qs in (self.failed_entries.contacts + self.failed_entries.calendars + self.failed_entries.events):
                qs.update(modified=timezone.now())
        finally:
            update_creds(self.user, self.credentials)

        logger.info(f"google.Synchronizer({self.user}): Sync summary ->\n{self.stats.to_rst()}")

        self._failed_entries = self.failed_entries
        self._stats = self.stats
        self.failed_entries = None
        self.stats = None
        return self

    def clear(self):
        self._failed_entries = self.failed_entries = self.user = self.stats = self._stats = self.credentials = None

    def sync(self, cal_only=False, contacts_only=False):
        self(cal_only, contacts_only)
        self.failed_entries = FailedEntries()
        self.stats = Stats()
        return self


class SynchronizeGoogle(dd.Action):
    help_text = _("Synchronize this database row with Google.")
    label = _("Sync Google")
    select_rows = True
    required_roles = dd.login_required()

    def run_from_ui(self, ar, **kwargs):
        if not ar.selected_rows:
            raise Exception
        for user in ar.selected_rows:
            Synchronizer(user)()
        ar.success()


dd.inject_action('users.User', synchronize_google=SynchronizeGoogle())


class Contacts(dd.Table):
    label = _("Google Contacts")
    model = 'google.Contact'
    required_roles = dd.login_required((SiteAdmin, SiteStaff))


class SyncableContacts(Contacts):
    label = _("Syncable Contacts")

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return rt.models.google.Contact.get_outward_insert_update_queryset()


class MyContacts(Contacts):
    required_roles = dd.login_required()
    insert_layout = """contact"""

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return super().get_request_queryset(ar, **filter).filter(user=ar.get_user())


class MySyncableContacts(SyncableContacts):
    required_roles = dd.login_required()

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return rt.models.google.Contact.get_outward_insert_update_queryset(ar.get_user())

class DeletedContacts(dd.Table):
    label = _("Deleted Contacts")
    model = "google.DeletedContact"
    required_roles = dd.login_required((SiteAdmin, SiteStaff))


class MyDeletedContacts(DeletedContacts):
    required_roles = dd.login_required()

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return super().get_request_queryset(ar, **filter).filter(user=ar.get_user())


class DeletedEntries(dd.Table):
    label = _("Deleted Cal Entries")
    model = "google.DeletedEntry"
    required_roles = dd.login_required((SiteAdmin, SiteStaff))


class MyDeletedEntries(DeletedEntries):
    required_roles = dd.login_required()

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return super().get_request_queryset(ar, **filter).filter(user=ar.get_user())


class SyncableEvents(dd.Table):
    label = _("Syncable Events")
    model = "cal.Event"
    required_roles = dd.login_required()

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = None
        for user, *_ in rt.models.google.CalendarSubscription.objects.values_list("user").distinct():
            if qs is None:
                qs = rt.models.cal.Event.get_outward_insert_update_queryset(user)
            else:
                qs = qs.union(rt.models.cal.Event.get_outward_insert_update_queryset(user))
        if qs is None:
            return rt.models.cal.Event.objects.none()
        return qs


class MySyncableEvents(SyncableEvents):

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return rt.models.cal.Event.get_outward_insert_update_queryset(ar.get_user())


DELETED_EVENTS_META = {}
DELETED_CALENDARS_META = {}

@dd.receiver(dd.post_analyze)
def set_delete_signal_receivers(*args, **kwargs):
    @dd.receiver(dd.pre_delete, sender=rt.models.cal.Event)
    def event_will_get_deleted(sender, instance, **kw):
        if instance.google_id and instance.synchronize_with_google():
            sub = rt.models.google.CalendarSubscription.objects.filter(
                models.Q(access_role='writer') | models.Q(access_role='owner'),
                calendar=instance.get_calendar()
            ).first()
            if sub is not None and (user := sub.user) is not None:
                DELETED_EVENTS_META[instance.google_id] = user

    @dd.receiver(dd.post_delete, sender=rt.models.cal.Event)
    def event_deleted(sender, instance, **kw):
        if user := DELETED_EVENTS_META.get(instance.google_id):
            entry = rt.models.google.DeletedEntry(event_id=instance.google_id, user=user,
                                                  calendar_id=instance.get_calendar().google_id)
            entry.full_clean()
            entry.save()
            del DELETED_EVENTS_META[instance.google_id]

    @dd.receiver(dd.pre_delete, sender=rt.models.cal.Calendar)
    def calendar_will_get_deleted(sender, instance, **kw):
        if instance.google_id:
            sub = rt.models.google.CalendarSubscription.objects.filter(
                models.Q(access_role='writer') | models.Q(access_role='owner'),
                calendar=instance
            ).first()
            if sub is not None and (user := sub.user):
                DELETED_CALENDARS_META[instance.google_id] = user

    @dd.receiver(dd.post_delete, sender=rt.models.cal.Calendar)
    def calendar_deleted(sender, instance, **kw):
        if user := DELETED_CALENDARS_META.get(instance.google_id):
            entry = rt.models.google.DeletedEntry(calendar_id=instance.google_id, calendar=True, user=user)
            entry.full_clean()
            entry.save()
            del DELETED_CALENDARS_META[instance.google_id]

    @dd.receiver(dd.post_save, sender=dd.resolve_model(dd.plugins.google.contacts_model))
    def contact_modified(sender, instance, **kw):
        for obj in rt.models.google.Contact.objects.filter(contact=instance):
            obj.full_clean()
            obj.save()

    @dd.receiver(dd.post_delete, sender=rt.models.google.Contact)
    def contact_deleted(sender, instance, **kw):
        inst = rt.models.google.DeletedContact(user=instance.user, contact_id=instance.google_id)
        inst.save_new_instance(ar=inst.get_default_table().request(user=instance.user))
