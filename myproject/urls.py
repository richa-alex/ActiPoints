from django.contrib import admin
from django.urls import path, include  # Import include
from myapp import views  # Import views from myapp

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', include('myapp.urls')),  
]
