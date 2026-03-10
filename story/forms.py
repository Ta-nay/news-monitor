from django import forms
from .models import Story


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            "title",
            "body_text",
            "url",
            "company",
            "tagged_companies",
        ]

        widgets = {
            "title": forms.TextInput(),
            "body_text": forms.Textarea(),
            "url": forms.URLInput(),
            "company": forms.Select(),
            "tagged_companies": forms.SelectMultiple(),
        }
