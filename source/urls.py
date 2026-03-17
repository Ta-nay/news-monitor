from django.urls import path
from .views import (
    SourceListView,
    SourceDeleteView,
    save_source,
    source_autocomplete,
)

# app_name = "sources"

urlpatterns = [
    path("add/", save_source, name="add_source"),
    path("", SourceListView.as_view(), name="source_list"),
    path(
        "<int:pk>/edit/",
        save_source,
        name="edit_source",
    ),
    path(
        "<int:pk>/delete/",
        SourceDeleteView.as_view(),
        name="delete_source",
    ),
    path("search/", source_autocomplete, name="source_autocomplete"),
]
