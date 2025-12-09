import random
from datetime import date, timedelta, time
from django.core.management.base import BaseCommand
from planner.models import Event, SoundEngineer

class Command(BaseCommand):
    help = 'Populates the database with sample schedule data for the next 4 weeks'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old events...')
        Event.objects.all().delete()
        
        self.stdout.write('Checking Sound Engineers...')
        engineers_data = [
            {'name': 'Mike Sound', 'email': 'mike@example.com', 'phone': '0712345678'},
            {'name': 'Sarah Audio', 'email': 'sarah@example.com', 'phone': '0723456789'},
            {'name': 'Tom Levels', 'email': 'tom@example.com', 'phone': '0734567890'},
        ]
        
        engineers = []
        for eng in engineers_data:
            obj, created = SoundEngineer.objects.get_or_create(
                name=eng['name'],
                defaults={
                    'contact_email': eng['email'],
                    'contact_number': eng['phone']
                }
            )
            engineers.append(obj)
            if created:
                self.stdout.write(f'Created engineer: {obj.name}')

        venues = ["The Blue Room", "Main Stage", "Jazz Corner", "Rooftop Bar", "Underground Club"]
        performers = [
            "The Rolling Stones Cover Band", "Jazz Trio", "DJ Snake", 
            "Acoustic Alice", "Rockin' Rob", "The Night Owls", 
            "Electric Dreams", "Salsa Squad"
        ]

        self.stdout.write('Creating new events...')
        
        today = date.today()
        # Start from this week's Monday
        start_date = today - timedelta(days=today.weekday())
        
        events_created = 0
        
        # Generate for 4 weeks
        for week in range(4):
            # Create 5-7 events per week
            num_events = random.randint(5, 7)
            
            # Get random days in this week (Mon-Sun)
            days_offsets = random.sample(range(7), num_events)
            days_offsets.sort()
            
            for offset in days_offsets:
                event_date = start_date + timedelta(weeks=week, days=offset)
                
                # Random start time between 18:00 and 22:00
                start_hour = random.randint(18, 22)
                start_time = time(start_hour, 0)
                
                # End time 2-4 hours later
                duration = random.randint(2, 4)
                end_hour = (start_hour + duration) % 24
                end_time = time(end_hour, 0)
                
                venue = random.choice(venues)
                performer = random.choice(performers)
                engineer = random.choice(engineers)
                
                Event.objects.create(
                    date=event_date,
                    performance_time_start=start_time,
                    performance_time_end=end_time,
                    venue=venue,
                    performer=performer,
                    sound_engineer=engineer,
                    event_notes=f"Standard setup for {performer}"
                )
                events_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {events_created} events over 4 weeks.'))
