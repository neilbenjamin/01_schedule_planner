from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

# Create your views here.


def accounts_index(request: HttpRequest) -> HttpRequest:
    """Accvess rerquest object data.
    Args:
        request (HttpRequest): Object
    Returns:
        HttpRequest: Return Http Response Object
    """
    return HttpResponse('<h2>This will become the profile page</h2>')


def user_login(request: HttpRequest) -> HttpRequest:
    """Request object data
    Args:
        request (HttpRequest): Login Data Object

    Returns:
        HttpRequest: Returns the login page html
    """
    return render(request, 'authentication/login.html')


def register(request: HttpRequest) -> HttpRequest:
    """Request object data from the register form.
    Args:
        request (HttpRequest): Register Form Object
    Returns:
        HttpRequest: Saved user details to the db and renders the signup
        html form.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print("Form errors:", form.errors)
        if form.is_valid():
            # Set Password
            user = form.save(commit=False)
            # Clean Inputs
            user.set_password(form.cleaned_data['password1'])
            # Save Form Input
            form.save()
            # Conditionally log user in if required, or redirect:
            # login(request, user)
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request, 'authentication/register.html', {'form': form})


def authenticate_user(request: HttpRequest) -> HttpRequest:
    """ Data Object
    Args:
        request (HttpRequest): User Login Data
    Returns:
        HttpRequest: Validates the user data submitted via the login page
    """
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        # Bind POST data to the form
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Authentication successful
                login(request, user)
                # Redirect to your schedule view after successful login
                return redirect('planner:index')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        # This block handles GET requests (initial page load for the form)
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {"form": form})


def logout_view(request: HttpRequest) -> HttpRequest:
    """GET Request Object
    Args:
        request (HttpRequest): GET Request
    Returns:
        HttpRequest: Get Requets to logout
    """
    logout(request)
    return redirect('accounts:login')

# Unused view for now. Will turn into profile view next


def show_user(request: HttpRequest) -> HttpRequest:
    """Request Object logged in user details
    Args:
        request (HttpRequest): Object

    Returns:
        HttpRequest: Return html with profile view
    """
    print(request.user.username)
    return render(request, 'authentication/user.html', {
        "username": request.user.username,
        "password": request.user.password
    })
