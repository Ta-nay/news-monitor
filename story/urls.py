from django.urls import path
from .views import add_story, StoryListView

urlpatterns = [
    path("add", add_story, name="add_story"),
    path("", StoryListView.as_view(), name="story_list"),
]
