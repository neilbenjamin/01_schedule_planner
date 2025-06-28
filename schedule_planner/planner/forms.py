# Import models/sql tables from models.py and the forms modules from Django.

from django import forms
from .models import Event, ContactMessage, SoundEngineer

# Create a new form sub class that we can build form objects with while tapping
# into Django's powerful pre-built bass or superclasses


class EventForm(forms.ModelForm):
    class Meta:
        # class attribute relevent to attribute instances
        model = Event
        # Attributes
        fields = [
            'date',
            'performance_time_start',
            'performance_time_end',
            'venue',
            'performer',
            'sound_engineer',
        ]
        # Widgets Dict for UI to pick dates and times
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'performance_time_start': forms.TimeInput(attrs={'type': 'time'}),
            'performance_time_end': forms.TimeInput(attrs={'type': 'time'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        # Define db model
        model = ContactMessage
        # define fields
        fields = [
            'name',
            'email',
            'message',
            # Will activate when form is live if needed
            # 'is_read',
            # 'replied_to'
        ]


# class EventEngineerUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['sound_engineer']
