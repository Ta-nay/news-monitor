from django.urls import path, include

from story.drf.apiviews import StoryListCreateAPIView, StoryDetailAPIView
from story.drf.functionals import story_list_create, story_detail
from story.drf.generics import StoryListCreateView, StoryDetailView
from rest_framework.routers import DefaultRouter

from story.drf.viewsets import StoryViewSet

router = DefaultRouter()
router.register(r"story", StoryViewSet, basename="story")

urlpatterns = [
    path("gen/", StoryListCreateView.as_view(), name="story-list-create"),
    path("gen/<int:pk>/", StoryDetailView.as_view(), name="story-detail"),
    path("api/", StoryListCreateAPIView.as_view(), name="story-list-create"),
    path("api/<int:pk>/", StoryDetailAPIView.as_view(), name="story-detail"),
    path("func/", story_list_create, name="story-list-create"),
    path("func/<int:pk>/", story_detail, name="story-detail"),
    path("",include(router.urls))
]