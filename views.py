from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import User  
from .models import Event  
from .form import EventForm  

def index(request):
    return render(request, 'index.html')

class StudentLoginView(auth_views.LoginView):
    template_name = 'student_login.html'

class FacultyLoginView(auth_views.LoginView):
    template_name = 'faculty_login.html'

class AdminLoginView(auth_views.LoginView):
    template_name = 'adminn_login.html'

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use .get() to avoid KeyError
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")  # Debug: Check form data

        user = authenticate(request, email=email, password=password)  # Use email for authentication
        print(f"User: {user}")  # Debug: Check if user is authenticated

        if user is not None and user.role == 'student':
            login(request, user)
            print("Login successful! Redirecting to student dashboard...")  # Debug
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a student.')
            print("Login failed!")  # Debug
    return render(request, 'student_login.html')

def faculty_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use .get() to avoid KeyError
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")  # Debug: Check form data

        user = authenticate(request, email=email, password=password)  # Use email for authentication
        print(f"User: {user}")  # Debug: Check if user is authenticated

        if user is not None and user.role == 'faculty':
            login(request, user)
            print("Login successful! Redirecting to faculty dashboard...")  # Debug
            return redirect('faculty_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a faculty.')
            print("Login failed!")  # Debug
    return render(request, 'faculty_login.html')

def adminn_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.role == 'admin':
            login(request, user)
            return redirect('adminn_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin.')
    return render(request, 'adminn_login.html')

@login_required
def student_dashboard(request):
    events = Event.objects.all() 
    # Check if the user has the 'student' role
    if not hasattr(request.user, 'role') or request.user.role != 'student':
        return redirect('index')  # Redirect non-students to the index page
    context = {
        'student': request.user,
        'events': events,  
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def faculty_dashboard(request):
    events = Event.objects.all()
    # Check if the user has the 'faculty' role
    if not hasattr(request.user, 'role') or request.user.role != 'faculty':
        return redirect('index')  # Redirect non-faculty to the index page
    context = {
        'faculty': request.user,
        'events': events,  
    }
    return render(request, 'faculty_dashboard.html', context)

@login_required
def adminn_dashboard(request):
    events = Event.objects.all()
    # Check if the user has the 'admin' role
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        return redirect('index')  # Redirect non-admin to the index page
    context = {
        'admin': request.user,
        'events': events,   
    }
    return render(request, 'adminn_dashboard.html', context)

# Submit Activity View
def submit_activity(request):
    return render(request, 'submit_activity.html')

# Fill Form View
def fill_form(request):
    return render(request, 'fill_form.html')

# Success View
def success(request):
    return render(request, 'success.html')

# Profile View
def profile(request):
    return render(request, 'profile.html')

# Rules View
def rules(request):
    return render(request, 'rules.html')

def student_management(request):
    if not request.user.is_staff:  # Ensure the user is an admin
        return redirect('index')

    if request.method == 'POST':
        # Handle form submission for adding/removing students
        if 'add_student' in request.POST:
            # Add student logic
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            regno = request.POST.get('regno')
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                regno=regno,
                role='student'
            )
        elif 'remove_student' in request.POST:
            # Remove student logic
            student_id = request.POST.get('student_id')
            User.objects.filter(id=student_id, role='student').delete()

    students = User.objects.filter(role='student')  # Fetch all students
    return render(request, 'student_management.html', {'students': students})

#faculty_management
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User

def faculty_management(request):
    if not request.user.is_staff:  # Ensure the user is an admin
        return redirect('index')

    if request.method == 'POST':
        # Handle form submission for adding/removing faculty
        if 'add_faculty' in request.POST:
            # Add faculty logic
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='faculty'
            )
        elif 'remove_faculty' in request.POST:
            # Remove faculty logic
            faculty_id = request.POST.get('faculty_id')
            User.objects.filter(id=faculty_id, role='faculty').delete()

    faculties = User.objects.filter(role='faculty')  # Fetch all faculty
    return render(request, 'faculty_management.html', {'faculties': faculties})

def upload_events(request):
    if not request.user.is_staff:  # Ensure only admins can access
        return redirect('index')

    if request.method == 'POST':
        if 'add_event' in request.POST:  # Handle event upload
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('upload_events')  # Refresh page
        elif 'delete_event' in request.POST:  # Handle event deletion
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            return redirect('upload_events')  # Refresh page

    else:
        form = EventForm()  # Render an empty form for GET requests

    # Fetch all events to display
    events = Event.objects.all()
    return render(request, 'upload_events.html', {'form': form, 'events': events})

def student_events(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'student_events.html', {'events': events})

def faculty_events(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'faculty_events.html', {'events': events})

# A_Profile View
def a_profile(request):
    if not request.user.is_staff:  # Ensure the user is an admin
        return redirect('index')
    
    # Pass the admin's details to the template
    context = {
        'admin': request.user,  # Pass the logged-in admin
    }
    return render(request, 'a_profile.html', context)
