from django.urls import path
from .views import add_company

urlpatterns = [
    path("add", add_company, name="add_company"),
]
