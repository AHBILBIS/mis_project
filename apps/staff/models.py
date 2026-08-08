from django.db import models
from apps.departments.models import Department

class StaffProfile(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_members")
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
