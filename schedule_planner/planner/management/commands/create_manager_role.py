from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from planner.models import SoundEngineer, Event


class Command(BaseCommand):
    help = 'Creates a management role for Sound Engineers'

    def handle(self, *args, **options):
        group_name = 'Engineer Managers'
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(f'Created new group: "{group_name}"')
        else:
            self.stdout.write(f'Found existing group: "{group_name}"')

        permissions_to_add = []

        # 1. Full CRUD for SoundEngineer
        ct_engineer = ContentType.objects.get_for_model(SoundEngineer)
        perms_engineer = Permission.objects.filter(content_type=ct_engineer)
        permissions_to_add.extend(perms_engineer)

        # 2. View and Change for Event
        ct_event = ContentType.objects.get_for_model(Event)
        perms_event = Permission.objects.filter(
            content_type=ct_event,
            codename__in=['view_event', 'change_event']
        )
        permissions_to_add.extend(perms_event)

        # 3. Add the custom permission "can_manage_event_engineer"
        try:
            perm_custom = Permission.objects.get(
                content_type=ct_event,
                codename='can_manage_event_engineer'
            )
            permissions_to_add.append(perm_custom)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Permission "can_manage_event_engineer" not found. '
                'Did you run migrations?'
            ))

        # Assign to group
        group.permissions.set(permissions_to_add)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully assigned {len(permissions_to_add)} permissions to '
            f'"{group_name}".'
        ))
        self.stdout.write(self.style.WARNING(
            'IMPORTANT: Users assigned to this group must also have '
            '"Staff status" (is_staff=True) to log in to the Admin site.'
        ))
