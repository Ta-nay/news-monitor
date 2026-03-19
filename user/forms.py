from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from company.models import Company

User = get_user_model()


class SignUp(UserCreationForm):

    company = forms.ModelChoiceField(
        queryset=Company.objects.none(), required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "company",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username
