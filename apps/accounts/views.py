from django.shortcuts import render, redirect
from django.http import HttpResponse
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

    html_login = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Management Information System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light d-flex align-items-center vh-100">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <div class="card shadow-sm border-0 rounded-3">
                    <div class="card-body p-4 p-sm-5">
                        <h3 class="card-title text-center mb-4 fw-bold">Sign In</h3>
                        <form method="POST">
                            <div class="mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input type="text" name="username" class="form-control" id="username" placeholder="Enter username" required autocomplete="username">
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" id="password" placeholder="Enter password" required autocomplete="current-password">
                            </div>
                            <button type="submit" class="btn btn-primary w-100 py-2 mt-2">Log In</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    return HttpResponse(html_login, content_type="text/html; charset=utf-8")


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
    html_dashboard = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">MIS Dashboard</a>
            <div class="d-flex">
                <a href="/accounts/logout/" class="btn btn-outline-light btn-sm">Logout</a>
            </div>
        </div>
    </nav>
    <div class="container">
        <div class="card shadow-sm">
            <div class="card-body">
                <h3>Welcome, {user.username}!</h3>
                <hr>
                <p><strong>Username:</strong> {user.username}</p>
                <p><strong>Email:</strong> {user.email}</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    return HttpResponse(html_dashboard, content_type="text/html; charset=utf-8")


@login_required
@role_required(['ADMIN', 'MANAGER'])
def manager_only_view(request):
    """
    Restricted manager panel view.
    """
    return HttpResponse("<h3>Manager Panel</h3>", content_type="text/html; charset=utf-8")