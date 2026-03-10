from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "url",
        ]
        widgets = {
            "name": forms.TextInput(),
            "url": forms.URLInput(),
        }
