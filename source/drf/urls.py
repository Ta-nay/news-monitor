from django.urls import path, include

from source.drf.apiviews import SourceListCreateAPIView, SourceDetailAPIView
from source.drf.functionals import source_list_create, source_detail
from source.drf.generics import SourceListCreateView, SourceDetailView
from rest_framework.routers import DefaultRouter
from source.drf.viewsets import SourceViewSet

router = DefaultRouter()
router.register(r"source", SourceViewSet, basename="source")


urlpatterns = [
    path("gen/", SourceListCreateView.as_view(), name="source-list-create"),
    path("gen/<int:pk>/", SourceDetailView.as_view(), name="source-detail"),
    path("api/", SourceListCreateAPIView.as_view(), name="source-list-create"),
    path("api/<int:pk>/", SourceDetailAPIView.as_view(), name="source-detail"),
    path("func/", source_list_create, name="source-list-create"),
    path("func/<int:pk>/", source_detail, name="source-detail"),
    path("",include(router.urls))
]