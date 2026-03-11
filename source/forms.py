from django import forms
from .models import Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = [
            "name",
            "url",
            "tagged_companies",
        ]

        widgets = {
            "name": forms.TextInput(),
            "url": forms.URLInput(),
            "tagged_companies": forms.SelectMultiple(),
        }
