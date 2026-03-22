import feedparser
from django import forms
from .models import Source
from company.models import Company


class SourceForm(forms.ModelForm):

    tagged_companies = forms.ModelMultipleChoiceField(
        queryset=Company.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "company-autocomplete"}),
        required=False,
    )

    class Meta:
        model = Source
        fields = ["name", "url", "tagged_companies"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.data.getlist("tagged_companies"):
            self.fields["tagged_companies"].queryset = Company.objects.filter(
                id__in=self.data.getlist("tagged_companies")
            )

    def clean_url(self):
        url = self.cleaned_data.get("url")
        feed = feedparser.parse(url)
        # feed.bozo == 1 means parsing failed
        if feed.bozo:
            raise forms.ValidationError("This is not a valid RSS feed.")
        if not feed.entries:
            raise forms.ValidationError("RSS feed has no entries.")
        return url
