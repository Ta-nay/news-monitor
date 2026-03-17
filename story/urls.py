from django.urls import path
from .views import (
    save_story,
    StoryListView,
    StoryDeleteView,
    story_autocomplete,
)

urlpatterns = [
    path("add/", save_story, name="add_story"),
    path("", StoryListView.as_view(), name="story_list"),
    path("<int:pk>/edit/", save_story, name="edit_story"),
    path("<int:pk>/delete/", StoryDeleteView.as_view(), name="delete_story"),
    path("search/", story_autocomplete, name="story_autocomplete"),
]
