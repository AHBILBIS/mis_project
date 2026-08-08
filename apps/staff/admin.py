from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "first_name", "last_name", "email", "designation", "hire_date")
    search_fields = ("employee_id", "first_name", "last_name", "email", "designation")
    list_filter = ("designation", "hire_date")

