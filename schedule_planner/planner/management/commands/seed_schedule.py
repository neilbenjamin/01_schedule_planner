import datetime
import random
from django.core.management.base import BaseCommand
from planner.models import Event, SoundEngineer, Venue, Performer


class Command(BaseCommand):
    help = 'Populates the database with specific schedule data from the provided screenshot'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Event.objects.all().delete()
        Venue.objects.all().delete()
        Performer.objects.all().delete()
        SoundEngineer.objects.all().delete()

        self.stdout.write('Creating Events from Screenshot Data...')

        # Data extracted from the screenshot
        # Format: (Date String, Venue Name, Performer Name, Start Time Str, End Time Str, Notes)
        raw_data = [
            ("Wed, Dec 3, 2025", "MGF", "DJ MARVIN", "19h30", "22h30", "MGF DRAW"),
            ("Wed, Dec 3, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "CORPORATE YEAR-END FUNCTIONS"),
            
            ("Thu, Dec 4, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "CORPORATE YEAR-END FUNCTIONS"),
            ("Thu, Dec 4, 2025", "TABLES - NON SMOKING", "DJ MARVIN", "18h15", "20h15", "BUGERS, BREWS & BLACKJACK"),

            ("Fri, Dec 5, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "CORPORATE YEAR-END FUNCTIONS"),
            ("Fri, Dec 5, 2025", "QUARTER DECK", "DJ MARVIN", "19h00", "22h00", "DINNER DANCE"),
            ("Fri, Dec 5, 2025", "PRIVE", "DJ AL", "17h00", "21h00", "RUGBY ACTIVATION"),

            ("Sat, Dec 6, 2025", "PRIVE", "DJ AL", "18h00", "21h00", "RUGBY ACTIVATION"),

            ("Sun, Dec 7, 2025", "PRIVE", "DJ MARVIN", "17h00", "20h00", "RUGBY ACTIVATION"),

            ("Wed, Dec 10, 2025", "MGF", "DJ MARVIN", "19h30", "22h30", "MGF DRAW"),
            ("Wed, Dec 10, 2025", "QUARTER DECK", "DJ ZAINO", "12h00", "15h00", "CORPORATE YEAR-END FUNCTIONS"),

            ("Thu, Dec 11, 2025", "QUARTER DECK", "DJ ZAINO", "12h00", "15h00", "CORPORATE YEAR-END FUNCTIONS"),
            ("Thu, Dec 11, 2025", "TABLES - NON SMOKING", "DJ KAYLAN", "18h15", "20h15", "BUGERS, BREWS & BLACKJACK"),

            ("Fri, Dec 12, 2025", "QUARTER DECK", "DJ MICHAEL", "12h00", "15h00", "CORPORATE YEAR-END FUNCTIONS"),
            ("Fri, Dec 12, 2025", "QUARTER DECK", "DJ MARVIN", "19h00", "22h00", "DINNER DANCE"),
            ("Fri, Dec 12, 2025", "PRIVE", "DJ AL", "19h00", "22h00", "ADDITIONAL DJ"),
            ("Fri, Dec 12, 2025", "FOODCOURT", "DJ ZAINO", "15h00", "18h00", "SUMMER ACTIVATION"),

            ("Sat, Dec 13, 2025", "PRIVE", "DJ MARVIN", "17h00", "22h30", "ADDITIONAL DJ"),
            ("Sat, Dec 13, 2025", "FOODCOURT", "DJ KAYLAN", "15h00", "18h00", "SUMMER ACTIVATION"),

            ("Mon, Dec 15, 2025", "PRIVE", "DJ KAYLAN", "20h00", "23h00", "SEASONAL CAMPAIGN EXTRA"),

            ("Tue, Dec 16, 2025", "PRIVE", "SIMPLY SWINGIN' TRIO", "20h00", "22h00", "SIMPLY SWINGIN' JAZZ TRIO"),
            ("Tue, Dec 16, 2025", "FOODCOURT", "DJ KAYLAN", "15h00", "18h00", "SUMMER ACTIVATION"),

            ("Wed, Dec 17, 2025", "MGF", "DJ AL", "19h30", "22h30", "MGF DRAW"),

            ("Thu, Dec 18, 2025", "TABLES - NON SMOKING", "DJ MAFAKU", "18h15", "20h15", "BUGERS, BREWS & BLACKJACK"),

            ("Fri, Dec 19, 2025", "MGF", "DJ KAYLAN", "18h00", "22h00", "BIRTHDAY ACTIVATION"),
            ("Fri, Dec 19, 2025", "QUARTER DECK", "DJ ASHLEY", "19h00", "22h00", "DINNER DANCE"),
            ("Fri, Dec 19, 2025", "PRIVE", "DJ MARVIN", "16h00", "23h00", "BIRTHDAY ACTIVATION + SEASONAL CAMPAIGN EXTRA"),
            ("Fri, Dec 19, 2025", "FOODCOURT", "DJ ZAINO", "15h00", "18h00", "SUMMER ACTIVATION"),
            ("Fri, Dec 19, 2025", "ATRIUM", "DJ ZAINO", "18h00", "20h00", "BIRTHDAY ACTIVATION"),

            ("Wed, Dec 24, 2025", "MGF", "DJ AI", "19h30", "22h30", "MGF DRAW"),
            ("Wed, Dec 24, 2025", "PRIVE", "DJ MARVIN", "18h00", "21h00", "SEASONAL CAMPAIGN EXTRA"),
            ("Wed, Dec 24, 2025", "FOODCOURT", "DJ KAYLAN", "14h00", "17h30", "SUMMER ACTIVATION"),

            ("Thu, Dec 25, 2025", "QUARTER DECK", "TAVARUA BAND", "12h00", "14h30", "XMAS LUNCH BAND"),
            ("Thu, Dec 25, 2025", "QUARTER DECK", "TAVARUA BAND", "15h00", "17h30", "XMAS LUNCH BAND"),
            ("Thu, Dec 25, 2025", "PRIVE", "DJ AL", "15h00", "20h00", "SEASONAL CAMPAIGN"),

            ("Fri, Dec 26, 2025", "QUARTER DECK", "DJ ASHLEY", "19h00", "22h00", "DINNER DANCE"),
            ("Fri, Dec 26, 2025", "PRIVE", "DJ AL", "08h00", "11h00", "BREAKFAST DJ"),
            ("Fri, Dec 26, 2025", "PRIVE", "DJ MARVIN", "19h00", "23h00", "SEASONAL CAMPAIGN"),
            ("Fri, Dec 26, 2025", "PRIVE", "SIMPLY SWINGIN' TRIO", "20h00", "22h00", "SIMPLY SWINGIN' JAZZ TRIO"),

            ("Sat, Dec 27, 2025", "PRIVE", "DJ MARVIN", "08h00", "11h00", "BREAKFAST DJ"),
            ("Sat, Dec 27, 2025", "PRIVE", "DJ KAYLAN", "19h00", "23h00", "SEASONAL CAMPAIGN"),
            ("Sat, Dec 27, 2025", "FOODCOURT", "DJ MARVIN", "15h00", "18h00", "SUMMER ACTIVATION"),

            ("Sun, Dec 28, 2025", "PRIVE", "DJ MARVIN", "08h00", "11h00", "BREAKFAST DJ"),
            ("Sun, Dec 28, 2025", "PRIVE", "DJ ASHLEY", "19h00", "23h00", "SEASONAL CAMPAIGN"),
            ("Sun, Dec 28, 2025", "FOODCOURT", "DJ KAYLAN", "15h00", "18h00", "SUMMER ACTIVATION"),

            ("Mon, Dec 29, 2025", "PRIVE", "DJ AL", "19h00", "23h00", "SEASONAL CAMPAIGN"),

            ("Tue, Dec 30, 2025", "PRIVE", "DJ AL", "08h00", "11h00", "BREAKFAST DJ"),
            ("Tue, Dec 30, 2025", "PRIVE", "DJ MARVIN", "19h00", "23h00", "SEASONAL CAMPAIGN"),

            ("Wed, Dec 31, 2025", "MGF", "DJ RITCHIE", "19h00", "23h00", "NYE DRAW"),
            ("Wed, Dec 31, 2025", "QUARTER DECK", "DJ KAYLAN", "19h00", "00h30", "NYE PARTY"),
            ("Wed, Dec 31, 2025", "PRIVE", "DJ KAYLAN", "08h00", "11h00", "BREAKFAST DJ"),
            ("Wed, Dec 31, 2025", "PRIVE", "DJ AL", "18h00", "02h00", "SEASONAL CAMPAIGN NYE PARTY"),
            ("Wed, Dec 31, 2025", "FOODCOURT", "DJ MARVIN", "19h30", "22h30", "NYE PARTY"),
            ("Wed, Dec 31, 2025", "NYE MARKET HALL", "DJ DANI B", "17h00", "01h00", "NYE PARTY"),
        ]

        for date_str, venue_name, performer_name, start_str, end_str, notes in raw_data:
            # Parse Date
            # "Wed, Dec 3, 2025"
            try:
                event_date = datetime.datetime.strptime(date_str, "%a, %b %d, %Y").date()
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Error parsing date {date_str}: {e}"))
                continue
            
            # Parse Time
            # "19h30"
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
            
            Event.objects.create(
                date=event_date,
                performance_time_start=start_time,
                performance_time_end=end_time,
                venue=venue,
                performer=performer,
                sound_engineer=None,
                event_notes=notes
            )
            self.stdout.write(f"Created event: {performer_name} at {venue_name} on {event_date}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded schedule from screenshot.'))
