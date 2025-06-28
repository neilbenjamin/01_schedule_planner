from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, permission_required
from .models import Event, ContactMessage
from .forms import EventForm, ContactForm
# from django.contrib import messages

# Create your views here.


@login_required
def index(request: HttpRequest) -> HttpRequest:
    """GET request that displays the main schedule for logged in users ordered
    by date and time.
    Args:
        request (HttpRequest): GET request

    Returns:
        HttpRequest: html page with the schedules
    """
    # Display full entertainment schedule
    events = Event.objects.all().order_by('date', 'performance_time_start')
    context = {
        'events': events,
    }
    if request.user.is_superuser:
        return render(request, 'pages/planner.html', context)
    else:
        return render(request, 'pages/planner_client.html', context)

    # return render(request, 'pages/planner.html', {'events': events})


@login_required
@permission_required('planner.add_event', raise_exception=True)
def add_event(request: HttpRequest) -> HttpRequest:
    """GET/POST request from form that either displays a blank, new form for
    registation on a GET request, or saves the details to the db for a POST
    request if the user is logged in.
    Args:
        request (HttpRequest): GET.POST Request Object

    Returns:
        HttpRequest: add user html template.
    """
    # Add new events to Events DB
    # Check CRUD method
    if request.method == 'POST':
        # create instance of EventForm with the values passed in the Http POST
        # object to variable 'form', which will be instatiated/populated with
        # the POSRT data
        form = EventForm(request.POST)
        # Check form validity
        if form.is_valid():
            # Save to DB
            form.save()
            # Redirect thereafter
            return redirect('planner:index')
    # conditional else return a blank form
    else:
        form = EventForm()
    # Serve the initial blank form on the initial GET request.
    return render(request, 'pages/add_event.html', {'form': form})


@login_required
@permission_required('planner.edit_event', raise_exception=True)
def edit_event(request: HttpRequest, pk: int) -> HttpRequest:
    """GET/POST Request object that retrieves the instance of the form and
    allows for editing and re-saving based on the pk, thereby updating the
    user, to logged in users.
    Args:
        request (HttpRequest): GET/POST Object
    Returns:
        HttpRequest: _description_Redirects to / or displays a blank for
        for error.
    """
    # Retrieve existing event record or 404 if not found.
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        # Bind/Instantiate object submitted data to form for validation
        # to the class EventForm
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('planner:index')
    else:
        form = EventForm(instance=event)
    return render(request, 'pages/add_event.html', {'form': form})


@login_required
@permission_required('planner.delete_view', raise_exception=True)
def delete_view(request: HttpRequest, pk: int) -> HttpRequest:
    """GET/POST request object that fetches the instance of the record
    based on the pk an removes it from the database, for logged in users.
    Args:
        request (HttpRequest):  GET/POST Object
        pk (int): _description_

    Returns:
        HttpRequest: Redirects users back to the / with the omitted record.
    """
    # Retrieve existing event record from model file with
    #  pk or 404 if not found.
    event = get_object_or_404(Event, pk=pk)
    # Conditional, if POST, delete
    if request.method == 'POST':
        # Update table with delete.
        event.delete()
        # Redirect to desired path.
        return redirect('planner:index')
        # No need for catching the inner Else as the dedault form actin
        # will manage these exceptions if the forms are not valid.
    else:
        # if method is GET or not POST, return the current form
        return render(request, 'pages/confirm_delete.html', {'event': event})


def contact_view(request: HttpRequest) -> HttpRequest:
    """Saves the users input from the contact form in the ContactMessage db
    and redirects to display page for testing purposes.
    Args:
        request (HttpRequest): GET/POST Object

    Returns:
        HttpRequest: Writes user data to the db and redirects to new display
        url.
    """
    # get form input
    if request.method == 'POST':
        # Bind user input
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            return redirect('planner:display_message', pk=contact_message.pk)
    else:
        form = ContactForm()
    # In case of a GET or error, return a blank form.
    return render(request, 'pages/contact.html', {'form': form})


def display_message(request: HttpRequest, pk: int) -> HttpRequest:
    """GET request object that reads the contents of the submitted
    user input from the contact form.
    Args:
        request (HttpRequest): GET Object
    Returns:
        HttpRequest: Displays the message.
    """
    message = get_object_or_404(ContactMessage, pk=pk)
    return render(request, 'pages/messages.html', {'message': message})


def conditions_view(request: HttpRequest) -> HttpRequest:
    """GET Request object thah displays the conditions of use.
    Args:
        request (HttpRequest): GET Object

    Returns:
        HttpRequest: Displays the conditions
    """
    return render(request, 'pages/conditions.html')
