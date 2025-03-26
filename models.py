from django.db import models
from django.contrib.auth.models import AbstractUser

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
