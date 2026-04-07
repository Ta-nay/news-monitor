from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from source.models import Source
from source.serializers import SourceSerializer


class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]
    filter_backends = [SearchFilter]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Source.objects
            .select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )
        if not user.is_staff:
        #     company_id = self.request.query_params.get("company_id")
        #     if company_id:
        #         queryset = queryset.filter(company_id=company_id)
        # else:
            queryset = queryset.filter(company_id=user.company_id)

        return queryset.order_by("-created_on")

    def perform_create(self, serializer):
        serializer.save(
            company = self.request.user.company,
            created_by = self.request.user,
            updated_by = self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}