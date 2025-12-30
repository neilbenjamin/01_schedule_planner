from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Event
from .utils.google_calendar import create_google_event, update_google_event, delete_google_event


@receiver(post_save, sender=Event)
def sync_event_to_google(sender, instance, created, **kwargs):
    """
    Signal to sync Django Event changes to Google Calendar.
    """
    # Avoid infinite recursion if we were to save the model inside the signal
    # (though we only update google_event_id which we should handle carefully)

    if created:
        # Create new event in Google Calendar
        google_id = create_google_event(instance)
        if google_id:
            # We need to save the ID back to the instance, but we must
            # avoid triggering the signal again.
            # We can use update() on the QuerySet to bypass signals, or a flag.
            Event.objects.filter(pk=instance.pk).update(google_event_id=google_id)
    else:
        # Update existing event
        # Check if we have a google_id, if not create one
        if not instance.google_event_id:
            google_id = create_google_event(instance)
            if google_id:
                Event.objects.filter(pk=instance.pk).update(google_event_id=google_id)
        else:
            update_google_event(instance)


@receiver(post_delete, sender=Event)
def delete_event_from_google(sender, instance, **kwargs):
    """
    Signal to delete event from Google Calendar when deleted in Django.
    """
    if instance.google_event_id:
        delete_google_event(instance.google_event_id, venue=instance.venue)
