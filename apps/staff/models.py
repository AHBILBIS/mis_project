from django.db import models
from django.conf import settings
from apps.departments.models import Department

class Staff(models.Model):
    """
    Operational HR profile model linked 1-to-1 with CustomUser.
    """
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'FT', 'Full Time'
        PART_TIME = 'PT', 'Part Time'
        CONTRACT = 'CT', 'Contract'
        INTERN = 'IN', 'Intern'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile'
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='staff_members'
    )
    job_title = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    employment_type = models.CharField(max_length=2, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField()
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Staff Records"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.job_title}"