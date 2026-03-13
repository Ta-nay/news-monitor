from django.urls import path
from .views import (
    add_source,
    SourceListView,
    SourceDeleteView,
    SourceUpdateView,
)

# app_name = "sources"

urlpatterns = [
    path("add/", add_source, name="add_source"),
    path("", SourceListView.as_view(), name="source_list"),
    path(
        "<int:pk>/edit/",
        SourceUpdateView.as_view(),
        name="edit_source",
    ),
    path(
        "<int:pk>/delete/", SourceDeleteView.as_view(),
        name="delete_source",
    ),
]
