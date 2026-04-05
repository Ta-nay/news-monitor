from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from source.models import Source
from source.serializers import SourceSerializer


class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]

    def get_queryset(self):
        queryset = (
            Source.objects
            .select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )
        company_id = self.request.query_params.get("company_id")
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)