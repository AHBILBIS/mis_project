from django.contrib import admin
from .models import StaffProfile  # Replace 'StaffProfile' with your actual model name

@admin.register(StaffProfile)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department']  # Add fields from your model to display