from django.urls import path
from .views import signup_view, SignInView, logout_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", logout_view, name="logout"),
]
