from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'job_title', 'employment_type', 'date_joined')
    list_filter = ('employment_type', 'department', 'gender')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'job_title')
    ordering = ('-date_joined',)