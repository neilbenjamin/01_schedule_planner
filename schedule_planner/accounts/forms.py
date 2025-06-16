from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class SignUpForm(UserCreationForm):
    """_summary_Extends the parent Django class
    Args:
        UserCreationForm (_type_): Parent Class
    """
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta(UserCreationForm.Meta):
        """Nested Class to specify the fields for for the form
        """
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('first_name',
                                                 'last_name',
                                                 'email')

# Test Form


class NameForm (forms.Form):
    your_name = forms.CharField(label="You Name", max_length=100)
    eye_colour = forms.CharField(label="Colour of your eyes", max_length=30)
