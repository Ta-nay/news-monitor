from django.urls import path

from company.views import company_autocomplete
from .views import add_company

urlpatterns = [
    path("add/", add_company, name="add_company"),
    path(
        "search/",
        company_autocomplete,
        name="company_autocomplete",
    ),
]
