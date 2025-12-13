import datetime
import random
from django.core.management.base import BaseCommand
from planner.models import Event, Venue, Performer, Activation


class Command(BaseCommand):
    help = 'Populates the database with specific schedule data from the provided screenshot'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Event.objects.all().delete()
        Venue.objects.all().delete()
        Performer.objects.all().delete()
        Activation.objects.all().delete()

        self.stdout.write('Creating Events from Screenshot Data...')

        # Data extracted from the screenshot
        # Format: (Date String, Venue Name, Performer Name, Start Time Str, End Time Str, Activation Name)
        raw_data = [
            ("Wed, Dec 03, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "YEAR-END"),
            ("Wed, Dec 03, 2025", "MGF", "DJ MARVIN", "19h30", "22h30", "MGF DRAW"),
            ("Thu, Dec 04, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "DINNER DANCE"),
            ("Thu, Dec 04, 2025", "TABLES - NON SMOKING", "DJ MARVIN", "18h15", "20h15", "BEATS, BREWS & BLACKJACK"),
            ("Fri, Dec 05, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "YEAR-END"),
            ("Fri, Dec 05, 2025", "PRIVE", "DJ AL", "17h00", "21h00", "RUGBY 7'S"),
            ("Fri, Dec 05, 2025", "QUARTER DECK", "DJ MARVIN", "19h00", "22h00", "DINNER DANCE"),
            ("Sat, Dec 06, 2025", "PRIVE", "DJ AL", "18h00", "21h00", "RUGBY 7'S"),
            ("Sun, Dec 07, 2025", "PRIVE", "DJ MARVIN", "17h00", "20h00", "RUGBY 7'S"),
            ("Wed, Dec 10, 2025", "QUARTER DECK", "DJ ZAINO", "12h00", "15h00", "YEAR-END"),
            ("Wed, Dec 10, 2025", "MGF", "DJ MARVIN", "19h30", "22h30", "MGF DRAW"),
            ("Thu, Dec 11, 2025", "QUARTER DECK", "DJ ZAINO", "12h00", "15h00", "YEAR-END"),
            ("Thu, Dec 11, 2025", "TABLES - NON SMOKING", "DJ KAYLAN", "18h15", "20h15", "BEATS, BREWS & BLACKJACK"),
            ("Fri, Dec 12, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "YEAR-END"),
            ("Fri, Dec 12, 2025", "FOODCOURT", "DJ ZAINO", "15h00", "18h00", "SUMMER CAMPAIGN"),
            ("Fri, Dec 12, 2025", "QUARTER DECK", "DJ MARVIN", "19h00", "22h00", "DINNER DANCE"),
            ("Fri, Dec 12, 2025", "PRIVE", "DJ AL", "19h00", "22h00", "150 SUPER LEAGUE"),
            ("Sat, Dec 13, 2025", "FOODCOURT", "DJ KAYLAN", "15h00", "18h00", "SUMMER CAMPAIGN"),
            ("Sat, Dec 13, 2025", "PRIVE", "DJ MARVIN", "17h00", "22h30", "150 SUPER LEAGUE"),
            ("Mon, Dec 15, 2025", "PRIVE", "DJ KAYLAN", "20h00", "23h00", "SUMMER CAMPAIGN"),
            ("Tue, Dec 16, 2025", "FOODCOURT", "DJ KAYLAN", "15h00", "18h00", "SUMMER CAMPAIGN"),
            ("Tue, Dec 16, 2025", "PRIVE", "SIMPLY SWINGIN' TRIO", "20h00", "22h00", "SUMMER CAMPAIGN"),
            ("Wed, Dec 17, 2025", "MGF", "DJ AL", "19h30", "22h30", "SUMMER CAMPAIGN"),
            ("Thu, Dec 18, 2025", "TABLES - NON SMOKING", "DJ MAFAKU", "18h15", "20h15", "BEATS, BREWS & BLACKJACK"),
            ("Fri, Dec 19, 2025", "FOODCOURT", "DJ ZAINO", "15h00", "18h00", "SUMMER CAMPAIGN"),
            ("Fri, Dec 19, 2025", "MGF", "DJ KAYLAN", "18h00", "22h00", "GW 25th BIRTHDAY"),
            ("Fri, Dec 19, 2025", "PRIVE", "DJ MARVIN", "18h00", "19h00", "GW 25th BIRTHDAY"),
            ("Fri, Dec 19, 2025", "ATRIUM", "DJ ZAINO", "18h00", "20h00", "GW 25th BIRTHDAY"),
            ("Fri, Dec 19, 2025", "QUARTER DECK", "DJ ASHLEY", "19h00", "22h00", "GW 25th BIRTHDAY"),
            ("Fri, Dec 19, 2025", "PRIVE", "DJ KAT LUTZ", "19h00", "23h00", "GW 25th BIRTHDAY"),
            ("Fri, Dec 19, 2025", "PRIVE", "DJ MARVIN", "23h00", "00h00", "GW 25th BIRTHDAY"),
            ("Wed, Dec 24, 2025", "FOODCOURT", "DJ KAYLAN", "14h00", "17h30", "CHRISTMAS EVE"),
            ("Wed, Dec 24, 2025", "PRIVE", "DJ MARVIN", "18h00", "21h00", "CHRISTMAS EVE"),
            ("Wed, Dec 24, 2025", "MGF", "DJ AI", "19h30", "22h30", "CHRISTMAS EVE"),
            ("Thu, Dec 25, 2025", "QUARTER DECK", "TAVARUA BAND", "12h00", "14h30", "CHRISTMAS DAY"),
            ("Thu, Dec 25, 2025", "QUARTER DECK", "TAVARUA BAND", "15h00", "17h30", "CHRISTMAS DAY"),
            ("Thu, Dec 25, 2025", "PRIVE", "DJ AL", "15h00", "20h00", "CHRISTMAS DAY"),
            ("Fri, Dec 26, 2025", "PRIVE", "DJ AL", "08h00", "11h00", "BREAKFAST BEATS"),
            ("Fri, Dec 26, 2025", "QUARTER DECK", "DJ ASHLEY", "19h00", "22h00", "DINNER DANCE"),
            ("Fri, Dec 26, 2025", "PRIVE", "DJ MARVIN", "19h00", "23h00", "SUMMER CAMPAIGN"),
            ("Fri, Dec 26, 2025", "PRIVE", "SIMPLY SWINGIN' TRIO", "20h00", "22h00", "SUMMER CAMPAIGN"),
            ("Sat, Dec 27, 2025", "PRIVE", "DJ MARVIN", "08h00", "11h00", "BREAKFAST BEATS"),
            ("Sat, Dec 27, 2025", "FOODCOURT", "DJ MARVIN", "15h00", "18h00", "SUMMER CAMPAIGN"),
            ("Sat, Dec 27, 2025", "PRIVE", "DJ KAYLAN", "19h00", "23h00", "SUMMER CAMPAIGN"),
            ("Sun, Dec 28, 2025", "PRIVE", "DJ MARVIN", "08h00", "11h00", "BREAKFAST BEATS"),
            ("Sun, Dec 28, 2025", "FOODCOURT", "DJ KAYLAN", "15h00", "18h00", "SUMMER CAMPAIGN"),
            ("Sun, Dec 28, 2025", "PRIVE", "DJ ASHLEY", "19h00", "23h00", "SUMMER CAMPAIGN"),
            ("Mon, Dec 29, 2025", "PRIVE", "DJ AL", "19h00", "23h00", "SUMMER CAMPAIGN"),
            ("Tue, Dec 30, 2025", "PRIVE", "DJ AL", "08h00", "11h00", "BREAKFAST BEATS"),
            ("Tue, Dec 30, 2025", "PRIVE", "DJ MARVIN", "19h00", "23h00", "SUMMER CAMPAIGN"),
            ("Wed, Dec 31, 2025", "PRIVE", "DJ KAYLAN", "08h00", "11h00", "BREAKFAST BEATS"),
            ("Wed, Dec 31, 2025", "NYE MARKET HALL", "DJ DANI B", "17h00", "01h00", "NYE PARTY"),
            ("Wed, Dec 31, 2025", "PRIVE", "DJ AL", "18h00", "02h00", "NYE PARTY"),
            ("Wed, Dec 31, 2025", "MGF", "DJ RITCHIE", "19h00", "23h00", "NYE PARTY"),
            ("Wed, Dec 31, 2025", "QUARTER DECK", "DJ KAYLAN", "19h00", "00h30", "NYE PARTY"),
            ("Wed, Dec 31, 2025", "FOODCOURT", "DJ MARVIN", "19h30", "22h30", "NYE PARTY"),
        ]

        for date_str, venue_name, performer_name, start_str, end_str, activation_name in raw_data:
            # Parse Date
            try:
                event_date = datetime.datetime.strptime(date_str, "%a, %b %d, %Y").date()
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Error parsing date {date_str}: {e}"))
                continue
            
            # Parse Time
            try:
                start_time = datetime.datetime.strptime(start_str, "%Hh%M").time()
                end_time = datetime.datetime.strptime(end_str, "%Hh%M").time()
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Error parsing time {start_str} or {end_str}: {e}"))
                continue

            # Get or Create Venue
            venue, _ = Venue.objects.get_or_create(name=venue_name)

            # Get or Create Performer
            performer, _ = Performer.objects.get_or_create(name=performer_name)

            # Get or Create Activation
            activation = None
            if activation_name:
                activation, _ = Activation.objects.get_or_create(name=activation_name)

            Event.objects.create(
                date=event_date,
                performance_time_start=start_time,
                performance_time_end=end_time,
                venue=venue,
                performer=performer,
                activation=activation
            )
            self.stdout.write(f"Created event: {performer_name} at {venue_name} on {event_date}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded schedule from screenshot.'))
