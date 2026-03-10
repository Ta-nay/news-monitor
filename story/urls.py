from django.urls import path
from .views import add_story

urlpatterns = [
    path("add", add_story, name="add_story"),
]
