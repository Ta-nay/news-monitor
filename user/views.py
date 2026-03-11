from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignUp
from source.models import Source


def signup_view(request):

    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.company = form.cleaned_data["company"]
            user.save()
            return redirect("signin")

    else:
        form = SignUp()

    return render(request, "user/signup.html", {"form": form})


class SignInView(LoginView):
    template_name = "user/signin.html"

    def get_success_url(self):
        if Source.objects.filter(created_by=self.request.user).exists():
            return reverse("source_list")
        return reverse("add_source")


@login_required
def logout_view(request):
    logout(request)
    return redirect("signin")
