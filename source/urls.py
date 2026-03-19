from django.urls import path
from .views import add_or_update, list_source, delete_source

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
    # path("search/", source_autocomplete, name="source_autocomplete"),
]
