import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schedule_planner.settings')
django.setup()

from planner.utils.google_calendar import get_calendar_service, CALENDAR_ID

def test_connection():
    print("Attempting to connect to Google Calendar...")
    service = get_calendar_service()
    
    if service:
        print("Successfully authenticated with Google!")
        try:
            # Try to list next 10 events to prove we have access
            print(f"Checking access to calendar: {CALENDAR_ID}")
            events_result = service.events().list(
                calendarId=CALENDAR_ID, 
                maxResults=5, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            if not events:
                print("Connection successful! No upcoming events found.")
            else:
                print(f"Connection successful! Found {len(events)} upcoming events:")
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(f"- {event['summary']} ({start})")
            
            print("\nSUCCESS: Your app can read/write to your Google Calendar.")
            
        except Exception as e:
            print(f"\nERROR: Authenticated, but failed to access the calendar.")
            print(f"Error details: {e}")
            print("Did you share the calendar with the service account email address?")
    else:
        print("\nERROR: Could not authenticate. Check service_account.json file.")

if __name__ == "__main__":
    test_connection()
