from django.contrib import admin
from .models import StaffProfile, InventoryItem, StaffReport, Sale, AuditLog, CartItem, Order, OrderItem

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'phone_number')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'sku', 'quantity', 'unit_price', 'department')

@admin.register(StaffReport)
class StaffReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('item', 'performed_by', 'quantity_sold', 'total_price', 'sold_at')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'total_amount', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'unit_price')
