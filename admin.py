from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Customize the User admin interface
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

    # Fields to filter by
    list_filter = ('role','is_staff', 'is_active')

    # Fields to include in the add/edit forms
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'role', 'regno')}),
        ('Permissions', {'fields': ('is_staff','is_active', 'is_superuser')}),
    )

    # Fields to include in the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'regno', 'is_staff', 'is_active'),
        }),
    )

# Register the User model with the custom admin interface
admin.site.register(User, CustomUserAdmin)