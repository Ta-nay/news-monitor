from django.urls import path
from .views import add_source, SourceListView

# app_name = "sources"

urlpatterns = [
    path("add", add_source, name="add_source"),
    path("", SourceListView.as_view(), name="source_list"),
]
