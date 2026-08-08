from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Human Resources"}),
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "HR"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
