from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, "departments/department_list.html", {"departments": departments})

@login_required
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully.")
            return redirect("department_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentForm()

    return render(request, "departments/department_form.html", {"form": form, "title": "Create Department"})
