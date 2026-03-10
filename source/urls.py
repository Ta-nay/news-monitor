from django.urls import path
from .views import add_source

urlpatterns = [path("add", add_source, name="add_source")]
