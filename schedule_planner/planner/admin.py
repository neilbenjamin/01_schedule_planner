from django.contrib import admin
from .models import Event, ContactMessage, SoundEngineer, Venue, Performer

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        # Check if user has the specific permission
        if (request.user.has_perm('planner.can_manage_event_engineer') and
                not request.user.is_superuser):
            # Return all fields EXCEPT 'sound_engineer' as read-only
            return [f.name for f in self.model._meta.fields
                    if f.name != 'sound_engineer']
        return super().get_readonly_fields(request, obj)


admin.site.register(Event, EventAdmin)
admin.site.register(ContactMessage)
admin.site.register(SoundEngineer)
admin.site.register(Venue)
admin.site.register(Performer)
