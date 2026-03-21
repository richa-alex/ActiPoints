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
    path('student/fill_form/', views.fill_form, name='fill_form'),
    path('submit-activity-form/', views.submit_activity_form, name='submit_activity_form'),
    path('student/submit_activity/fill_form/success/', views.success, name='success'),
    path('student/profile/', views.profile, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='profile.html',success_url='/profile/'), name='password_change'),
    path('student/events/', views.student_events, name='student_events'),
    path('student/rules/', views.rules, name='rules'),
    path('success/', views.success, name='success'),
    path('progress/', views.progress, name='student_progress'),
    path('progress/<int:student_id>/', views.student_progress, name='student_progress'),
    path('forgot-password/', views.forgot_pass, name='forgot_pass'),

    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/requests/', views.faculty_requests, name='faculty_requests'),
    path('faculty/process/<int:submission_id>/', views.process_submission, name='process_submission'),
    path('faculty/student_display/', views.student_display, name='student_display'),  # List view
    path('faculty/student_display/<int:regno>/', views.student_display, name='student_detail'),  # Detail view
    path('faculty/approve-activity/', views.approve_activity, name='approve_activity'),
    path('faculty/reject-activity/', views.reject_activity, name='reject_activity'),
    path('faculty/faculty_events/', views.faculty_events, name='faculty_events'),

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
    
