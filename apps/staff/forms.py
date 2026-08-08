from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["item_name", "sku", "quantity", "unit_price"]
        widgets = {
            "item_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item name"}),
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "SKU code"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}),
        }

