from django.urls import path
from . import views

urlpatterns = [
    # Storefront & Cart routes
    path('store/', views.store_home, name='store_home'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.customer_dashboard, name='customer_dashboard'),

    # Staff Directory routes
    path('list/', views.staff_list, name='staff_list'),
    path('create/', views.staff_create, name='staff_create'),

    # Inventory Management routes
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/create/', views.inventory_create, name='inventory_create'),
    path('inventory/edit/<int:item_id>/', views.inventory_edit, name='inventory_edit'),
    path('inventory/delete/<int:item_id>/', views.inventory_delete, name='inventory_delete'),
    path('inventory/export/', views.export_inventory_excel, name='export_inventory_excel'),

    # Word Report route
    path('report/create/', views.create_report, name='create_report'),
]

