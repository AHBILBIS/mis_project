from django.contrib import admin
from .models import StaffProfile, InventoryItem, StaffReport

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "department", "phone")
    search_fields = ("department__name", "phone")

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "sku", "quantity", "unit_price", "last_updated")
    list_filter = ("last_updated",)
    search_fields = ("item_name", "sku")

@admin.register(StaffReport)
class StaffReportAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "author__username")

