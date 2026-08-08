from django.urls import path
from . import views

urlpatterns = [
    path("", views.staff_list, name="staff_list"),
    path("add/", views.staff_create, name="staff_create"),
    path("report/new/", views.create_report, name="create_report"),
    path("inventory/", views.inventory_list, name="inventory_list"),
    path("inventory/add/", views.inventory_create, name="inventory_create"),
    path("inventory/<int:pk>/edit/", views.inventory_edit, name="inventory_edit"),
    path("inventory/export/", views.export_inventory_excel, name="export_inventory_excel"),
]
