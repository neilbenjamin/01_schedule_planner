from django.core.management.base import BaseCommand
from planner.models import Event, Venue
from planner.utils.google_calendar import list_upcoming_events
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = 'Sync events from Google Calendar to Django'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting Google Calendar sync...')
        # 1 Get all venues that have a Google Calendar ID.
        venues = (Venue.objects.exclude(google_calendar_id__isnull=True)
                  .exclude(google_calendar_id__exact=''))

        for venue in venues:
            self.stdout.write(f"Checking venue: {venue.name} "
                              f"({venue.google_calendar_id})with Calendar ID: "
                              f"{venue.google_calendar_id})")
            # 2 Fetch events from Google for this venue
            google_events = (list_upcoming_events(calendar_id=venue.
                                                  google_calendar_id))

            for g_event in google_events:
                # 3 Extract data (ID. summary. start time)
                g_id = g_event.get('id')
                summary = g_event.get('summary')
                start_data = g_event.get('start', {})
                end_data = g_event.get('end', {})
                # Parse times (Gogole gives strings, we need Pythin objects)
                start_iso = start_data.get('dateTime', start_data.get('date'))
                end_iso = end_data.get('dateTime', end_data.get('date'))
                # Convert string "2025-12-31T20:00..." to a real
                # datetime object
                start_dt = parse_datetime(start_iso)
                end_dt = parse_datetime(end_iso)

                if not start_dt or not end_dt:
                    continue  # Skip if dates are weird.

                # THE CORE LOGIC : FIND AND UPDATE
                try:
                    # try to find the event in our DB using the GOogle ID.
                    event = Event.objects.get(google_event_id=g_id)

                    # Check if the time has changed
                    if event.date != start_dt.date() or \
                        event.performance_time_start != start_dt.time() or \
                            event.performance_time_end != end_dt.time():

                        (self.stdout.
                         write(self.style.SUCCESS(f" UPDATING {summary}")))

                        # Update the database (bypassing
                        # signals to avoids loops)
                        Event.objects.filter(pk=event.pk).update(
                            date=start_dt.date(),
                            performance_time_start=start_dt.time(),
                            performance_time_end=end_dt.time()
                        )
                except Event.DoesNotExist:
                    (self.stdout.
                     write(self.style.
                           WARNING(f" Skipping external event: {summary}")))
