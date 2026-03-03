from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Custom User model to handle roles (student, faculty, admin)
class User(AbstractUser):
    first_name = None
    last_name = None

    ROLES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )
    regno = models.CharField(max_length=10, blank=True, null=True)  
    role = models.CharField(max_length=10, choices=ROLES, default='student')

class Activity(models.Model):
    event_title = models.CharField(max_length=200)
    zone = models.TextField()
    category = models.TextField()
    points = models.TextField()
    achievement = models.TextField()
    date = models.DateField()
    certificate = models.ImageField(upload_to='')

    def __str__(self):
        return self.title
    
class Event(models.Model):
    title = models.CharField(max_length=200)  # Event title
    description = models.TextField()  # Event description
    poster = models.ImageField(upload_to='event_posters/')  # Event poster image
    date = models.DateField()  # Event date

    def __str__(self):
        return self.title

class ActivityCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

        
class StudentProfile(models.Model):  # Note the colon at the end
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username

class ActivitySubmission(models.Model):
    # Define status choices first
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    event_title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    rejection_reason = models.TextField(blank=True, null=True)
    points = models.PositiveIntegerField()
    student = models.IntegerField()
    category = category = models.CharField(max_length=255)
    event_title = models.CharField(max_length=200)
    points = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_submissions')
    rejection_reason = models.TextField(blank=True)
    
    # Category-specific fields (using JSON for flexibility)
    details = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.student.username} - {self.event_title}"

class Certificate(models.Model):
    submission = models.ForeignKey(ActivitySubmission, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to='certificates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

