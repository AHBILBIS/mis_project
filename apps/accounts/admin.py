from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'employee_id', 'role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Enterprise Information', {'fields': ('role', 'employee_id', 'phone_number', 'profile_picture', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Enterprise Information', {'fields': ('role', 'employee_id', 'phone_number', 'is_verified')}),
    )