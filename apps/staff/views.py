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

import io
from django.http import HttpResponse
from docx import Document
import openpyxl
from .models import InventoryItem, StaffReport

@login_required
def create_report(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        # Save to database
        report = StaffReport.objects.create(title=title, author=request.user, content=content)
        
        # Generate Word Document (.docx)
        doc = Document()
        doc.add_heading(title, 0)
        doc.add_paragraph(f"Author: {request.user.username}")
        doc.add_paragraph(f"Date: {report.created_at.strftime(\"%Y-%m-%d %H:%M\")}")
        doc.add_heading("Report Summary", level=1)
        doc.add_paragraph(content)

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response["Content-Disposition"] = f"attachment; filename=\"{title}.docx\""
        doc.save(response)
        return response

    return render(request, "staff/create_report.html")

@login_required
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, "staff/inventory_list.html", {"items": items})

@login_required
def export_inventory_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory Summary"

    # Header Row
    headers = ["ID", "Item Name", "SKU", "Quantity", "Unit Price ($)"]
    ws.append(headers)

    # Data Rows
    for item in InventoryItem.objects.all():
        ws.append([item.id, item.item_name, item.sku, item.quantity, float(item.unit_price)])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=\"Inventory_Report.xlsx\""
    wb.save(response)
    return response

