from django.urls import path, include
from django.contrib.auth import views as auth_views
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('student/login/', views.student_login, name='student_login'),
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('adminn/login/', views.adminn_login, name='adminn_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/submit_activity/', views.submit_activity, name='submit_activity'),
    path('student/submit_activity/fill_form/', views.fill_form, name='fill_form'),
    path('student/submit_activity/fill_form/success/', views.success, name='success'),
    path('student/profile/', views.profile, name='profile'),
    path('student/rules/', views.rules, name='rules'),
    path('student/events/', views.student_events, name='student_events'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('adminn/dashboard/', views.adminn_dashboard, name='adminn_dashboard'),
    path('adminn/student_management/', views.student_management, name='student_management'),
    path('adminn/faculty_management/', views.faculty_management, name='faculty_management'),
    path('adminn/upload_events/', views.upload_events, name='upload_events'),
    path('adminn/a_profile/', views.a_profile, name='a_profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
