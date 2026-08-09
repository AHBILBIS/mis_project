from django.urls import path
from . import views

urlpatterns = [
    path("", views.staff_list, name="staff_list"),
    path("add/", views.staff_create, name="staff_create"),
    path("inventory/", views.inventory_list, name="inventory_list"),
    path("inventory/add/", views.inventory_create, name="inventory_create"),
    path("inventory/export/", views.export_inventory_excel, name="export_inventory_excel"),
    path("sales/", views.sales_list, name="sales_list"),
    path("sales/new/", views.record_sale, name="record_sale"),
    path("audit-logs/", views.audit_log_list, name="audit_logs"),
    path("report/new/", views.create_report, name="create_report"),
]
