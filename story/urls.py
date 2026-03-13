from django.urls import path
from .views import add_story, StoryListView, StoryDeleteView, StoryUpdateView

urlpatterns = [
    path("add/", add_story, name="add_story"),
    path("", StoryListView.as_view(), name="story_list"),
    path("<int:pk>/edit/", StoryUpdateView.as_view(), name="edit_story"),
    path("<int:pk>/delete/", StoryDeleteView.as_view(), name="delete_story"),
]