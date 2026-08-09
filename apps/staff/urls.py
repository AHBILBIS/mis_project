from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store_home, name='store_home'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.customer_dashboard, name='customer_dashboard'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/edit/<int:item_id>/', views.inventory_edit, name='inventory_edit'),
    path('inventory/delete/<int:item_id>/', views.inventory_delete, name='inventory_delete'),
]

