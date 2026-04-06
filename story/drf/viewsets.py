from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from story.models import Story
from story.serializers import StorySerializer


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["title", "body_text"]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Story.objects
            .select_related("company", "source", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .order_by("-created_on")
        )

        if user.is_staff:
            company_id = self.request.query_params.get("company_id")
            if company_id:
                queryset = queryset.filter(company_id=company_id)
        else:
            queryset = queryset.filter(company=user.company)

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)