
"""working urls"""
from django.urls import path, include
from .views import add_or_update, list_source, delete_source, new_sources

# app_name = "sources"

urlpatterns = [
    path("add/", add_or_update, name="add_source"),
    path("", list_source, name="source_list"),
    path(
        "<int:id>/edit/",
        add_or_update,
        name="edit_source",
    ),
    path(
        "<int:id>/delete/",
        delete_source,
        name="delete_source",
    ),
    path("new", new_sources, name="ang_sources"),
]
