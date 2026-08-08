from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg

# Django REST Framework Imports
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.decorators import role_required
from apps.departments.models import Department
from apps.staff.models import Staff
from apps.staff.serializers import StaffSerializer, DepartmentSerializer, RegisterSerializer
from apps.staff.permissions import IsAdminOrReadOnly
from apps.staff.exports import export_staff_csv, export_staff_excel


# ==========================================
# 1. HTML Authentication & User Views
# ==========================================

def user_login(request):
    """
    Standard HTML login view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    """
    Logs out the current user and redirects to login page.
    """
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """
    Renders the primary dashboard for the logged-in user.
    """
    user = request.user
    staff_profile = getattr(user, 'staff_profile', None)

    context = {
        'user': user,
        'staff_profile': staff_profile,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
@role_required(['ADMIN', 'MANAGER'])
def manager_only_view(request):
    """
    Restricted manager panel view.
    """
    return render(request, 'accounts/manager_panel.html')

from .forms import UserRegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            if hasattr(user, "role"):
                user.role = "STAFF"
                user.save()

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})

