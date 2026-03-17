from django import forms
from story.models import Story
from company.models import Company


class StoryForm(forms.ModelForm):
    tagged_companies = forms.ModelMultipleChoiceField(
        queryset=Company.objects.none(), required=False
    )

    class Meta:
        model = Story
        fields = [
            "title",
            "body_text",
            "url",
            "tagged_companies",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.getlist("tagged_companies"):
            self.fields["tagged_companies"].queryset = Company.objects.filter(
                id__in=self.data.getlist("tagged_companies")
            )
