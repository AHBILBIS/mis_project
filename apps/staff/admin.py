from django.contrib import admin
from .models import StaffProfile, InventoryItem, StaffReport, Sale, AuditLog

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

