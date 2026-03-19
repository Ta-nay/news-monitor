from django.urls import path
from .views import add_or_update, list_story, delete_story

urlpatterns = [
    path("add/", add_or_update, name="add_story"),
    path("", list_story, name="story_list"),
    path("<int:id>/edit/", add_or_update, name="edit_story"),
    path("<int:id>/delete/", delete_story, name="delete_story"),
    # path("search/", story_autocomplete, name="story_autocomplete"),
]
