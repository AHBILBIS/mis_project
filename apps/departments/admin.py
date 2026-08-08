from django.contrib import admin
from .models import Department  # Replace 'Department' with your actual model name

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Add fields from your model to display