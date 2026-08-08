import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from docx import Document
import openpyxl

from .models import StaffProfile, InventoryItem, StaffReport
from .forms import StaffProfileForm

@login_required
def staff_list(request):
    staff_members = StaffProfile.objects.select_related("user", "department").all()
    return render(request, "staff/staff_list.html", {"staff_members": staff_members})

@login_required
def staff_create(request):
    if request.method == "POST":
        form = StaffProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member created successfully.")
            return redirect("staff_list")
    else:
        form = StaffProfileForm()
    return render(request, "staff/staff_form.html", {"form": form})

@login_required
def create_report(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        report = StaffReport.objects.create(
            title=title, 
            author=request.user, 
            content=content
        )
        
        doc = Document()
        doc.add_heading(title, 0)
        doc.add_paragraph(f"Author: {request.user.username}")
        
        formatted_date = report.created_at.strftime("%Y-%m-%d %H:%M")
        doc.add_paragraph(f"Date: {formatted_date}")
        
        doc.add_heading("Report Summary", level=1)
        doc.add_paragraph(content)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
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

    headers = ["ID", "Item Name", "SKU", "Quantity", "Unit Price ($)"]
    ws.append(headers)

    for item in InventoryItem.objects.all():
        ws.append([item.id, item.item_name, item.sku, item.quantity, float(item.unit_price)])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=\"Inventory_Report.xlsx\""
    wb.save(response)
    return response

