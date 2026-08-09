from django import forms
from .models import StaffProfile, InventoryItem, Sale

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ["department", "phone"]
        widgets = {
            "department": forms.Select(attrs={"class": "form-select"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["department", "item_name", "sku", "quantity", "unit_price"]
        widgets = {
            "department": forms.Select(attrs={"class": "form-select"}),
            "item_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item name"}),
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "SKU code"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["item", "quantity_sold"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-select"}),
            "quantity_sold": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }

