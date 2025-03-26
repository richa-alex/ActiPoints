from django import forms
from .models import Activity
from .models import Event


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['event_title', 'zone', 'category', 'points', 'achievement', 'certificate']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'poster', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Add a date picker
        }