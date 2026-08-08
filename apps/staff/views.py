from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import StaffProfile
from .forms import StaffProfileForm

@login_required
def staff_list(request):
    query = request.GET.get("q", "")
    staff_members = StaffProfile.objects.all()

    if query:
        staff_members = staff_members.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(designation__icontains=query)
        )

    return render(request, "staff/staff_list.html", {"staff_members": staff_members, "query": query})

@login_required
def staff_create(request):
    if request.method == "POST":
        form = StaffProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully.")
            return redirect("staff_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StaffProfileForm()

    return render(request, "staff/staff_form.html", {"form": form, "title": "Add New Staff"})
