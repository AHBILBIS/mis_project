import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from docx import Document
from .models import InventoryItem, StaffProfile

@login_required
def store_home(request):
    items = InventoryItem.objects.all() if "InventoryItem" in globals() else []
    return render(request, "store/store_home.html", {"items": items})

@login_required
def cart_view(request):
    return render(request, "store/cart.html")

@login_required
def add_to_cart(request, item_id):
    return redirect("store_home")

@login_required
def checkout(request):
    return redirect("store_home")

@login_required
def customer_dashboard(request):
    return render(request, "store/customer_dashboard.html")

@login_required
def staff_list(request):
    query = request.GET.get("q", "")
    profiles = StaffProfile.objects.all() if "StaffProfile" in globals() else []
    return render(request, "staff/staff_list.html", {"profiles": profiles, "query": query})

@login_required
def staff_create(request):
    return render(request, "staff/staff_form.html")

@login_required
def inventory_list(request):
    items = InventoryItem.objects.all() if "InventoryItem" in globals() else []
    return render(request, "staff/inventory_list.html", {"items": items})

@login_required
def inventory_create(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        sku = request.POST.get("sku")
        quantity = request.POST.get("quantity", 0)
        unit_price = request.POST.get("unit_price", 0.0)
        InventoryItem.objects.create(
            item_name=item_name,
            sku=sku,
            quantity=quantity,
            unit_price=unit_price
        )
        return redirect("inventory_list")
    return render(request, "staff/inventory_form.html")

@login_required
def inventory_edit(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == "POST":
        item.item_name = request.POST.get("item_name", item.item_name)
        item.sku = request.POST.get("sku", item.sku)
        item.quantity = request.POST.get("quantity", item.quantity)
        item.unit_price = request.POST.get("unit_price", item.unit_price)
        item.save()
        return redirect("inventory_list")
    return render(request, "staff/inventory_edit.html", {"item": item})

@login_required
def inventory_delete(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    item.delete()
    return redirect("inventory_list")

@login_required
def export_inventory_excel(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=inventory.csv"
    writer = csv.writer(response)
    writer.writerow(["SKU", "Item Name", "Quantity", "Unit Price"])
    for item in InventoryItem.objects.all():
        writer.writerow([item.sku, item.item_name, item.quantity, item.unit_price])
    return response

@login_required
def create_report(request):
    if request.method == "POST":
        title = request.POST.get("title", "MIS Report")
        author = request.POST.get("author", "Staff")
        body_text = request.POST.get("content", "")

        doc = Document()
        doc.add_heading(title, 0)
        doc.add_paragraph(f"Author: {author}")
        doc.add_paragraph("----------------------------------------")
        doc.add_paragraph(body_text)

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        response["Content-Disposition"] = "attachment; filename=report.docx"
        return response

    return render(request, "staff/report_form.html")