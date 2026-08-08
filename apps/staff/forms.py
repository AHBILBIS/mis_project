from django import forms
from .models import StaffProfile

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ["employee_id", "first_name", "last_name", "email", "phone", "department", "designation", "salary", "hire_date"]
        widgets = {
            "employee_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "EMP-1001"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
            "salary": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "hire_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
