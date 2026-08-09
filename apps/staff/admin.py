from django.contrib import admin
from .models import StaffProfile, InventoryItem, StaffReport, Sale, AuditLog, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "customer__username", "shipping_address")
    inlines = [OrderItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "quantity", "created_at")

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "department", "phone")

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "sku", "department", "quantity", "unit_price")

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("item", "quantity_sold", "total_price", "performed_by", "sold_at")

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "details")
    list_filter = ("timestamp", "action")

@admin.register(StaffReport)
class StaffReportAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")