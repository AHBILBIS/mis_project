from django.db import models
from django.conf import settings
from apps.departments.models import Department

class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.department}"

class InventoryItem(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} ({self.sku})"

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.quantity * self.item.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.item.item_name} (User: {self.user.username})"

class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    order_number = models.CharField(max_length=50, unique=True)
    shipping_address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer.username} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.item.item_name if self.item else 'Deleted Item'}"

class Sale(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="sales")
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.quantity_sold}x {self.item.item_name}"

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.user} - {self.action}"

class StaffReport(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title