from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.decorators import role_required
from .forms import UserRegisterForm

def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html", {"user": request.user})

@login_required
@role_required(["ADMIN", "MANAGER"])
def manager_only_view(request):
    return render(request, "accounts/manager_panel.html")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

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

