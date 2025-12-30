import logging
import calendar
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .utils.google_calendar import sync_events_from_google
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, EventForm
from .models import ContactMessage, Event

logger = logging.getLogger(__name__)
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
    # Get year and month from query params, default to today
    today = date.today()
    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
    except ValueError:
        year = today.year
        month = today.month

    # Calculate previous and next month for navigation
    first_day = date(year, month, 1)

    # Previous month
    prev_month_date = first_day - timedelta(days=1)
    prev_year = prev_month_date.year
    prev_month = prev_month_date.month

    # Next month
    # Get last day of current month, add 1 day
    _, last_day_num = calendar.monthrange(year, month)
    next_month_date = date(year, month, last_day_num) + timedelta(days=1)
    next_year = next_month_date.year
    next_month = next_month_date.month

    # Display full entertainment schedule for the selected month
    events = Event.objects.filter(
        date__year=year, date__month=month
    ).order_by("date", "performance_time_start")

    context = {
        "events": events,
        "current_year": year,
        "current_month": month,
        "current_month_name": calendar.month_name[month],
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    }
    if request.user.is_superuser or request.user.has_perm(
        "planner.can_manage_event_engineer"
    ):
        return render(request, "pages/planner.html", context)
    else:
        return render(request, "pages/planner_client.html", context)

    # return render(request, 'pages/planner.html', {'events': events})


def send_event_notification(event, action_type):
    """Sends email notification to all users about an event change."""
    subject = f"Schedule Update: {action_type} - {event.venue}"
    # Format times to remove seconds (HH:MM)
    start_time = event.performance_time_start.strftime("%H:%M")
    end_time = event.performance_time_end.strftime("%H:%M")

    message = f"""
<p>Hi,</p>

<p>A schedule update has been made.</p>

<p>
Action: {action_type}<br>
Venue: {event.venue}<br>
Date: {event.date}<br>
Time: {start_time} - {end_time}<br>
Performer: {event.performer}<br>
Activation: {event.activation}
</p>

<p>Please check the <a href="https://planner.capedjco.co.za/">schedule</a>
for full details.</p>
"""
    # Get all user emails, exclude those without emails
    recipient_list = list(
        User.objects.exclude(email="").values_list("email", flat=True)
    )

    if recipient_list:
        logger.info(f"Sending notification to {len(recipient_list)} users.")
        try:
            # Send to DEFAULT_FROM_EMAIL, BCC everyone else to protect privacy
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # To
                recipient_list,  # BCC
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            logger.info("Notification sent successfully.")
        except Exception as e:
            logger.error(f"Error sending notification: {e}")


@login_required
@permission_required("planner.add_event", raise_exception=True)
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
    if request.method == "POST":
        # create instance of EventForm with the values passed in the Http POST
        # object to variable 'form', which will be instatiated/populated with
        # the POSRT data
        form = EventForm(request.POST)
        # Check form validity
        if form.is_valid():
            # Save to DB
            event = form.save()

            # Check if user requested notification
            if request.POST.get("action") == "notify":
                send_event_notification(event, "New Event Added")

            # Redirect thereafter
            return redirect("planner:index")
    # conditional else return a blank form
    else:
        form = EventForm()
    # Serve the initial blank form on the initial GET request.
    return render(request, "pages/add_event.html", {"form": form})


@login_required
@permission_required("planner.edit_event", raise_exception=True)
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
    if request.method == "POST":
        # Bind/Instantiate object submitted data to form for validation
        # to the class EventForm
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()

            # Check if user requested notification
            if request.POST.get("action") == "notify":
                send_event_notification(event, "Event Updated")

            return redirect("planner:index")
    else:
        form = EventForm(instance=event)
    return render(request, "pages/add_event.html", {"form": form})


@login_required
@permission_required("planner.delete_view", raise_exception=True)
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
    if request.method == "POST":
        # Update table with delete.
        event.delete()
        # Redirect to desired path.
        return redirect("planner:index")
        # No need for catching the inner Else as the dedault form actin
        # will manage these exceptions if the forms are not valid.
    else:
        # if method is GET or not POST, return the current form
        return render(request, "pages/confirm_delete.html", {"event": event})


def contact_view(request: HttpRequest) -> HttpRequest:
    """Saves the users input from the contact form in the ContactMessage db
    and redirects to display page for testing purposes.
    Args:
        request (HttpRequest): GET/POST Object

    Returns:
        HttpRequest: Writes user data to the db and redirects to new display
        url.
    """
    logger.info(f"Contact view called. Method: {request.method}")
    # get form input
    if request.method == "POST":
        # Bind user input
        form = ContactForm(request.POST)
        if form.is_valid():
            logger.info("Form is valid. Saving...")
            contact_message = form.save()

            # Send email
            subject = f"New Contact Message from {contact_message.name}"
            message = (
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n\n"
                f"Message:\n{contact_message.message}"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.DEFAULT_FROM_EMAIL]

            logger.info(
                f"Attempting to send email to "
                f"{recipient_list} from {from_email}..."
            )
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=False,
                )
                logger.info("Email sent successfully.")
            except Exception as e:
                logger.error(f"Error sending email: {e}")

            return redirect("planner:display_message", pk=contact_message.pk)
        else:
            logger.warning(f"Form is invalid. Errors: {form.errors}")
    else:
        form = ContactForm()
    # In case of a GET or error, return a blank form.
    return render(request, "pages/contact.html", {"form": form})


def display_message(request: HttpRequest, pk: int) -> HttpRequest:
    """GET request object that reads the contents of the submitted
    user input from the contact form.
    Args:
        request (HttpRequest): GET Object
    Returns:
        HttpRequest: Displays the message.
    """
    message = get_object_or_404(ContactMessage, pk=pk)
    return render(request, "pages/messages.html", {"message": message})


def conditions_view(request: HttpRequest) -> HttpRequest:
    """GET Request object thah displays the conditions of use.
    Args:
        request (HttpRequest): GET Object

    Returns:
        HttpRequest: Displays the conditions
    """
    return render(request, "pages/conditions.html")


# Sync Google Calendar events view
@login_required
def sync_calendar_view(request: HttpRequest) -> HttpRequest:
    """
    View to trigger Google Calendar sync and display results manually.
    Args: request (HttpRequest): GET Request
    """
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to sync "
                                "calendars.")
        return redirect("planner:index")

    # run the sync
    sync_messages = sync_events_from_google()

    # Show feedback to user
    updated_count = 0
    if sync_messages:
        updated_count = sum(1 for msg in sync_messages if 'Updated:' in msg)

    if updated_count > 0:
        messages.success(request, f"Sync Complete: {updated_count} event(s) updated from Google Calendar.")
    else:
        messages.info(request, "Sync Complete. No changes found.")

    return redirect('planner:index')
