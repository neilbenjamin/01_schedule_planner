import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'service_account.json')
# The ID of the calendar to sync with. 
# For a service account, if you share your personal calendar with the service account email,
# this should be your personal email address (e.g., 'neil@example.com').
# If using the service account's own calendar, use 'primary'.
# CALENDAR_ID = 'primary' 

def get_calendar_service():
    """
    Authenticates and returns the Google Calendar service.
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logger.warning(f"Service account file not found at {SERVICE_ACCOUNT_FILE}. Google Calendar sync will be skipped.")
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
        # 2. Fallback to 'primary' (the service account's own calendar) or a global default
        calendar_id = 'primary'
        if event_instance.venue and event_instance.venue.google_calendar_id:
            calendar_id = event_instance.venue.google_calendar_id
        
        event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
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
