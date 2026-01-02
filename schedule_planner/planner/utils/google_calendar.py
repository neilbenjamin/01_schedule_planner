import os
import logging
import datetime
from planner.models import Event, Venue
from django.utils.dateparse import parse_datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = settings.GOOGLE_SERVICE_ACCOUNT_FILE
# The ID of the calendar to sync with.
# For a service account, if you share your personal calendar with
# the service account email,
# this should be your personal email address (e.g., 'neil@example.com').
# If using the service account's own calendar, use 'primary'.
# CALENDAR_ID = 'primary'


def list_upcoming_events(calendar_id="primary", max_results=50):
    """
    Fetches upcoming events from Google Calendar.
    """
    service = get_calendar_service()
    if not service:
        return []

    try:
        # 'Z" indicates UTC Time
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events

    except Exception as e:
        logger.error(f"Error fetching Google Calendar Events: {e}")
        return []


def get_calendar_service():
    """
    Authenticates and returns the Google Calendar service.
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logger.warning(
            f"Service account file not found at {SERVICE_ACCOUNT_FILE}."
            f" Google Calendar sync will be skipped.")
        return None

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Failed to create Google Calendar service: {e}")
        return None


def create_google_event(event_instance):
    """
    Creates an event in Google Calendar from a Django Event instance.
    Returns the Google Event ID.
    """
    service = get_calendar_service()
    if not service:
        return None

    event_body = _build_event_body(event_instance)

    try:
        # Determine which calendar ID to use
        # 1. Try the venue's specific calendar ID
        # 2. Fallback to 'primary' (the service account's own calendar) or
        # a global default
        calendar_id = 'primary'
        if event_instance.venue and event_instance.venue.google_calendar_id:
            calendar_id = event_instance.venue.google_calendar_id

        event = service.events().insert(calendarId=calendar_id,
                                        body=event_body).execute()
        logger.info(f"Created Google Calendar event: {event.get('id')} on calendar {calendar_id}")
        return event.get('id')
    except Exception as e:
        logger.error(f"Error creating Google Calendar event: {e}")
        return None


def update_google_event(event_instance):
    """
    Updates an existing event in Google Calendar.
    """
    if not event_instance.google_event_id:
        return create_google_event(event_instance)

    service = get_calendar_service()
    if not service:
        return None

    event_body = _build_event_body(event_instance)

    try:
        # Determine which calendar ID to use
        calendar_id = 'primary'
        if event_instance.venue and event_instance.venue.google_calendar_id:
            calendar_id = event_instance.venue.google_calendar_id

        updated_event = service.events().update(
            calendarId=calendar_id,
            eventId=event_instance.google_event_id,
            body=event_body
        ).execute()
        logger.info(f"Updated Google Calendar event: {updated_event.get('id')} on calendar {calendar_id}")
        return updated_event.get('id')
    except Exception as e:
        logger.error(f"Error updating Google Calendar event: {e}")
        return None


def delete_google_event(google_event_id, venue=None):
    """
    Deletes an event from Google Calendar.
    """
    if not google_event_id:
        return

    service = get_calendar_service()
    if not service:
        return

    try:
        # Determine which calendar ID to use
        calendar_id = 'primary'
        if venue and venue.google_calendar_id:
            calendar_id = venue.google_calendar_id

        service.events().delete(calendarId=calendar_id, eventId=google_event_id).execute()
        logger.info(f"Deleted Google Calendar event: {google_event_id} from calendar {calendar_id}")
    except Exception as e:
        logger.error(f"Error deleting Google Calendar event: {e}")


def _build_event_body(event):
    """
    Helper to construct the Google Calendar event body dictionary.
    """
    # Combine date and time
    start_datetime = f"{event.date}T{event.performance_time_start}"
    end_datetime = f"{event.date}T{event.performance_time_end}"
    
    description = (
        f"Performer: {event.performer.name}\n"
        f"Venue: {event.venue.name}\n"
        f"Activation: {event.activation.name if event.activation else 'None'}\n"
        f"Contact: {event.performer.contact_number or 'N/A'}"
    )

    return {
        'summary': f"{event.performer.name} @ {event.venue.name}",
        'location': event.venue.address or event.venue.name,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': settings.TIME_ZONE, 
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': settings.TIME_ZONE,
        },
    }


def sync_events_from_google():
    """
    Syncs events from Google Calendar to Django.
    Returns a list of status messages.
    """
    messages = []
    venues = Venue.objects.exclude(google_calendar_id__isnull=True).exclude(google_calendar_id__exact='')
    for venue in venues:
        messages.append(f"Checking venues: {venue.name}")
        google_events = list_upcoming_events(calendar_id=venue.google_calendar_id)

        for g_event in google_events:
            g_id = g_event.get('id')
            summary = g_event.get('summary')
            start_data = g_event.get('start', {})
            end_data = g_event.get('end', {})

            start_iso = start_data.get('dateTime', start_data.get('date'))
            end_iso = end_data.get('dateTime', end_data.get('date'))

            start_dt = parse_datetime(start_iso)
            end_dt = parse_datetime(end_iso)

            if not start_dt or not end_dt:
                continue
            try:
                event = Event.objects.get(google_event_id=g_id)

                if event.date != start_dt.date() or \
                    event.performance_time_start != start_dt.time() or \
                        event.performance_time_end != end_dt.time():

                    Event.objects.filter(pk=event.pk).update(
                        date=start_dt.date(),
                        performance_time_start=start_dt.time(),
                        performance_time_end=end_dt.time()
                    )
                    messages.append(f"Updated: {summary}")
            except Event.DoesNotExist:
                pass  # Skipping external event silently.

    return messages
