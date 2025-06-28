from django.db import models

# Create your models here.

# New sound engineer model linked to Event one to many as a foreign
# key.


class SoundEngineer(models.Model):
    """Sound engineer we can assign to various events"""
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    """Create a database table module for the details of the the event and
    the booking.
    """
    # Table Col data
    date = models.DateField()
    performance_time_start = models.TimeField(verbose_name="Start Time")
    performance_time_end = models.TimeField(verbose_name="End Time")
    venue = models.CharField(max_length=100)
    performer = models.CharField(max_length=100)
    sound_engineer = models.ForeignKey(SoundEngineer,
                                       on_delete=models.SET_NULL,
                                       blank=True,
                                       null=True,
                                       related_name='events_as_engineer')
    event_notes = models.TextField(verbose_name="Event notes",
                                   blank=True, null=True)

    def __str__(self):
        """Human readable string from Event object
        Returns:
            _type_: String of performer and date
        """
        return f"{self.performer} on {self.date} in {self.venue}"

    class Meta:
        ordering = ['date', 'performance_time_start']
        permissions = [
            ("can_manage_event_engineer", "can_assign_engineers")
        ]


class ContactMessage(models.Model):
    """Creates a table in the db of the user message created by the
    form. It also cretaes a date-stamp and has additional booleans which we
    will impliment when I have teh 3rd paryt email service implimented.
    """
    # Content of table
    name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="Your email address")
    message = models.TextField(verbose_name="Your message")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    replied_to = models.BooleanField(default=False)
    # foromat for admin

    def __str__(self):
        """Inherit Django Model superclass.
    Args:
        models Module and superclass
    Returns:
        _type_: Sub Class and Instance attributes
        """
        formatted_time = self.created_at.strftime('%B %d, %Y at %I:%M %p')
        return f"from {self.name} on {formatted_time}"
