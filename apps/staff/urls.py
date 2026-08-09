from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Redirect /staff/ directly to /staff/store/
    path('', RedirectView.as_view(url='store/', permanent=False)),

    path('list/', views.staff_list, name='staff_list'),
    path('create/', views.staff_create, name='staff_create'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/create/', views.inventory_create, name='inventory_create'),
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/record/', views.record_sale, name='record_sale'),
    path('audit-logs/', views.audit_log_list, name='audit_log_list'),
    path('reports/create/', views.create_report, name='create_report'),
    path('inventory/export/excel/', views.export_inventory_excel, name='export_inventory_excel'),
    
    # E-Commerce & Storefront Routes
    path('store/', views.store_home, name='store_home'),
    path('store/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
]
