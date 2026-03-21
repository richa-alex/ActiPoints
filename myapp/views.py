from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import User, Event, ActivitySubmission
from .form import EventForm
from .models import ActivityCategory, ActivitySubmission, Certificate, StudentProfile
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import json 
from django.db import connection



def index(request):
    return render(request, 'index.html')

class StudentLoginView(auth_views.LoginView):
    template_name = 'student_login.html'

class FacultyLoginView(auth_views.LoginView):
    template_name = 'faculty_login.html'

class AdminLoginView(auth_views.LoginView):
    template_name = 'adminn_login.html'

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect

User = get_user_model()

def forgot_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_pass')

        try:
            user = User.objects.get(email=email, role='student')  # Adjust role if needed
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password has been reset. You can now log in.")
            return redirect('student_login')
        except User.DoesNotExist:
            messages.error(request, "No student found with that email.")

    return render(request, 'forgot_pass.html')



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
    # Ensure default categories exist
    default_categories = [
        "National Initiatives",
        "Sports & Games",
        "Cultural Activities",
        "Professional Self Initiatives",
        "Entrepreneurship & Innovation",
        "Leadership & Management"
    ]
    
    for name in default_categories:
        ActivityCategory.objects.get_or_create(name=name)
    
    return render(request, 'submit_activity.html')

def fill_form(request):
    category_name = request.GET.get('category', '')
    try:
        # Verify the category exists
        category = ActivityCategory.objects.get(name=category_name)
        return render(request, 'fill_form.html', {'category': category_name})
    except ActivityCategory.DoesNotExist:
        # If category doesn't exist, redirect back
        return redirect('submit_activity')
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.files.storage import FileSystemStorage
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def submit_activity_form(request):
    if request.method == 'POST':
        try:
            # Get form data
            event_title = request.POST.get('eventTitle')
            category = request.POST.get('category')
            points = request.POST.get('points')

            print(request.POST.get('certificates'))

            category_obj = ActivityCategory.objects.get(name=category)
            cat_id = category_obj.id

            # Prepare details dictionary based on category
            details = {}
            
            if category == 'National Initiatives':
                details.update({
                    'event_type': request.POST.get('eventType'),
                    'additional_activity': request.POST.get('additionalActivity')
                })
            elif category in ['Sports & Games', 'Cultural Activities']:
                details.update({
                    'achievement': request.POST.get('achievement'),
                    'zone': request.POST.get('zone'),
                    'additional_activity': request.POST.get('additionalActivity', '')
                })
            elif category == 'Entrepreneurship & Innovation':
                details.update({
                    'achievement': request.POST.get('achievement'),
                    'additional_activity': request.POST.get('additionalActivity', '')
                })

            # Create activity submission
            submission = ActivitySubmission(
                student=request.user.id,
                category=cat_id,
                event_title=event_title,
                points=points,
                details=details
            )
            
            submission.save()
            
            # Handle file uploads
            files = request.FILES.getlist('certificates')
            for file in files:
                Certificate.objects.create(
                    submission=submission,
                    file=file
                )
            
            return JsonResponse({
                'success': True, 
                'redirect': ('student_dashboard')
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False, 
        'message': 'Invalid request method'
    })
@login_required
def success(request):
    return render(request, 'success.html')





@login_required
def progress(request):
    user_id = request.user.id

    try:
        with connection.cursor() as cursor:
            # Fetch approved submissions
            cursor.execute(
                "SELECT * FROM myapp_activitysubmission WHERE student = %s AND status = 'approved'", 
                [user_id]
            )
            approved = cursor.fetchall()

            # Fetch pending submissions
            cursor.execute(
                "SELECT * FROM myapp_activitysubmission WHERE student = %s AND status = 'pending'", 
                [user_id]
            )
            pending = cursor.fetchall()

            # Fetch rejected submissions
            cursor.execute(
                "SELECT * FROM myapp_activitysubmission WHERE student = %s AND status = 'rejected'", 
                [user_id]
            )
            rejected = cursor.fetchall()

        # Process submissions
        def process(submissions):
            processed = []
            for sub in submissions:
                sub = list(sub)
                try:
                    sub[7] = json.loads(sub[7])  # assuming 'details' is at index 7
                except (json.JSONDecodeError, IndexError):
                    sub[7] = {}
                processed.append(sub)
            return processed

        approved_submissions = process(approved)
        pending_submissions = process(pending)
        rejected_submissions = process(rejected)

        # Calculate total points (assuming 'points' is at index 2)
        total_points = sum(sub[2] for sub in approved if sub[2] is not None)
        progress_percentage = min((total_points / 100) * 100, 100) if approved else 0

        return render(request, 'progress.html', {
            'approved_submissions': approved_submissions,
            'pending_submissions': pending_submissions,
            'rejected_submissions': rejected_submissions,
            'total_points': total_points,
            'progress_percentage': progress_percentage
        })

    except Exception as e:
        print(f"Error in progress view: {str(e)}")
        return HttpResponse("An error occurred while processing your request", status=500)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import json

@login_required
def student_progress(request, student_id):
    try:
        with connection.cursor() as cursor:
            # Fetch approved submissions
            cursor.execute(
                "SELECT * FROM myapp_activitysubmission WHERE student = %s AND status = 'approved'", 
                [student_id]
            )
            approved = cursor.fetchall()

            # Fetch pending submissions
            cursor.execute(
                "SELECT * FROM myapp_activitysubmission WHERE student = %s AND status = 'pending'", 
                [student_id]
            )
            pending = cursor.fetchall()

            # Fetch rejected submissions
            cursor.execute(
                "SELECT * FROM myapp_activitysubmission WHERE student = %s AND status = 'rejected'", 
                [student_id]
            )
            rejected = cursor.fetchall()

        # Process submissions
        def process(submissions):
            processed = []
            for sub in submissions:
                sub = list(sub)
                try:
                    sub[7] = json.loads(sub[7])  # assuming 'details' is at index 7
                except (json.JSONDecodeError, IndexError):
                    sub[7] = {}
                processed.append(sub)
            return processed

        approved_submissions = process(approved)
        pending_submissions = process(pending)
        rejected_submissions = process(rejected)

        # Calculate total points (assuming 'points' is at index 2)
        total_points = sum(sub[2] for sub in approved if sub[2] is not None)
        progress_percentage = min((total_points / 100) * 100, 100) if approved else 0

        return render(request, 'progress.html', {
            'approved_submissions': approved_submissions,
            'pending_submissions': pending_submissions,
            'rejected_submissions': rejected_submissions,
            'total_points': total_points,
            'progress_percentage': progress_percentage
        })

    except Exception as e:
        print(f"Error in student_progress view: {str(e)}")
        return HttpResponse("An error occurred while processing the student’s progress", status=500)



@login_required
def faculty_requests(request):
    
    user_id = request.user.id
    query = "SELECT *  FROM myapp_activitysubmission AS a LEFT JOIN myapp_certificate AS c ON c.submission_id = a.id LEFT JOIN myapp_user AS u ON u.id = a.student;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        submissions = cursor.fetchall()

    processed_submissions = []
    for submission in submissions:
        try:
            activity_data = json.loads(submission[7])  # Convert JSON string to dict
            submission = list(submission)  # Convert tuple to list (to modify)
            submission[7] = activity_data  # Replace with dict
        except json.JSONDecodeError:
            submission[7] = {}  # Default empty dict if parsing fails
        processed_submissions.append(submission)
    print(submissions[20])
    return render(request, 'requests.html', {
        'submissions': processed_submissions
    })

@login_required
def process_submission(request, submission_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == 'POST':
        try:
            submission = ActivitySubmission.objects.get(id=submission_id)
            action = request.POST.get('action')
            
            if action == 'approve':
                submission.status = 'approved'
                submission.processed_by = request.user
                submission.save()
                
                # Update student's points
                profile, created = StudentProfile.objects.get_or_create(user=submission.student)
                profile.total_points += submission.points
                profile.save()
                
            elif action == 'reject':
                submission.status = 'rejected'
                submission.processed_by = request.user
                submission.rejection_reason = request.POST.get('reason', '')
                submission.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from myapp.models import User  # Update as per your app structure

def student_display(request, regno=None):
    if not request.user.is_authenticated or request.user.role != 'faculty':
        return redirect('index')

    # Single student detail view
    if regno is not None:
        student = get_object_or_404(User, id=regno, role='student')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(points), 0)
                FROM myapp_activitysubmission
                WHERE student_id = %s AND status = 'approved'
            """, [student.id])
            points = cursor.fetchone()[0]

        return render(request, 'student_display.html', {
            'student': student,
            'points': points
        })

    # Student list view
    else:
        search_query = request.GET.get('search', '')

        with connection.cursor() as cursor:
            if search_query:
                cursor.execute("""
                    SELECT u.id, u.username, u.email, u.regno,
                           (SELECT COALESCE(SUM(points), 0)
                            FROM myapp_activitysubmission a
                            WHERE a.student = u.id AND a.status = 'approved') AS total_points
                    FROM myapp_user u
                    WHERE u.role = 'student' AND (
                        LOWER(u.username) LIKE LOWER(%s) OR 
                        LOWER(u.email) LIKE LOWER(%s) OR 
                        LOWER(u.regno) LIKE LOWER(%s)
                    )
                """, [f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'])
            else:
                cursor.execute("""
                    SELECT u.id, u.username, u.email, u.regno,
                           (SELECT COALESCE(SUM(points), 0)
                            FROM myapp_activitysubmission a
                            WHERE a.student = u.id AND a.status = 'approved') AS total_points
                    FROM myapp_user u
                    WHERE u.role = 'student'
                """)
            
            student_rows = cursor.fetchall()

        students = [
            {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'regno': row[3],
                'points': row[4],
            } for row in student_rows
        ]

        return render(request, 'student_display.html', {
            'students': students,
            'search_query': search_query
        })

# Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('profile')
       
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'profile.html', {
        'form': form,
        'user': request.user  # Make sure user object is passed to template
    })

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

    # Fetch all students and order by username (name)
    students = User.objects.filter(role='student').order_by('regno')
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


@csrf_exempt  # Only for development. Use proper CSRF handling in production.
def approve_activity(request):
    if request.method == "POST":
        activity_id = request.POST.get("activity_id")
        print(activity_id)
        try:
            activity = ActivitySubmission.objects.get(id=activity_id.replace("activity-", ""))
            activity.status = "approved"  # Update status
            activity.save()
            return JsonResponse({"success": True})
        except Activity.DoesNotExist:
            return JsonResponse({"success": False, "message": "Activity not found"})
    return JsonResponse({"success": False, "message": "Invalid request"})

# views.py
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
@login_required
def approve_activity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            activity = ActivitySubmission.objects.get(id=data['activity_id'])
            activity.status = "approved"
            activity.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid method"}, status=405)

@ensure_csrf_cookie
@login_required
def reject_activity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            activity = ActivitySubmission.objects.get(id=data['activity_id'])
            activity.status = "rejected"
            activity.rejection_reason = data['reason']
            activity.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": False, "message": "Invalid method"}, status=405)


