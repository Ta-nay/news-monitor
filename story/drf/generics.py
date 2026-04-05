"""generic views"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from story.models import Story
from story.serializers import StorySerializer


class StoryListCreateView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = (
            Story.objects
            .select_related("company", "source", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .order_by("-created_on")
        )
        company_id = self.request.query_params.get("company_id")
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    def perform_create(self, serializer):
        serializer.save(
            created_by = self.request.user,
            updated_by = self.request.user,
            source_id = None
        )


class StoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StorySerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Story.objects
            .select_related("company", "source", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)