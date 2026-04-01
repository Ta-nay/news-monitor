"""generic views"""

from rest_framework import generics
from source.models import Source
from source.serializers import SourceSerializer


class SourceListCreateView(generics.ListCreateAPIView):
    serializer_class = SourceSerializer
    def get_queryset(self):
        return (
            Source.objects
            .select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

class SourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SourceSerializer
    def get_queryset(self):
        return (
            Source.objects
            .select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)