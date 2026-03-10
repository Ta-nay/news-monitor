from django import forms
from .models import Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = [
            "name",
            "url",
            "company",
            "tagged_companies",
        ]

        widgets = {
            "name": forms.TextInput(),
            "url": forms.URLInput(),
            "company": forms.Select(),
            "tagged_companies": forms.SelectMultiple(),
        }
