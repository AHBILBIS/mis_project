from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .decorators import role_required

def user_login(request):
    """Handles user login authentication."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """Handles user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def dashboard(request):
    """Central landing page for authenticated users showing role-specific info."""
    context = {
        'user': request.user,
        'role': request.user.get_role_display(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
@role_required(['ADMIN', 'MANAGER'])
def manager_only_view(request):
    """Example restricted view accessible only to Admins and Managers."""
    return render(request, 'accounts/manager_panel.html')