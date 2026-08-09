code = '''from django import forms
from .models import StaffProfile, InventoryItem, Sale

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['department', 'phone_number']

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['item_name', 'sku', 'quantity', 'unit_price', 'department']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['item', 'quantity_sold']
'''

with open('apps/staff/forms.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: Updated apps/staff/forms.py!")