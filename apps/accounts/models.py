from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    """
    Enterprise Custom User Model extending Django's built-in AbstractUser.
    Includes Role-Based Access Control (RBAC) choices and profile metadata.
    """
    
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'System Administrator'
        MANAGER = 'MANAGER', 'Department Manager'
        STAFF = 'STAFF', 'Operational Staff'
        AUDITOR = 'AUDITOR', 'Auditor'

    # Enterprise attributes for RBAC
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STAFF,
        help_text="Designates user role for system permissions."
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    employee_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Signal: Automatically create an auth token for newly registered users
@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Automatically generate a REST API Token whenever a new CustomUser is created.
    """
    if created:
        Token.objects.create(user=instance)