"""class based views"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from story.models import Story
from story.serializers import StorySerializer



class StoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class StoryListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        stories = (
            Story.objects
            .select_related("company", "source", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
            .order_by("-created_on")
        )
        company_id = request.query_params.get("company_id")
        if company_id:
            stories = stories.filter(company_id=company_id)
        paginator = StoryPagination()
        page = paginator.paginate_queryset(stories, request, view=self)
        serializer = StorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request):
        serializer = StorySerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                updated_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(
            Story.objects
            .select_related("company", "source", "created_by", "updated_by")
            .prefetch_related("tagged_companies"),
            pk=pk
        )

    def get(self, request, pk):
        story = self.get_object(pk)
        serializer = StorySerializer(story)
        return Response(serializer.data)

    def put(self, request, pk):
        story = self.get_object(pk)
        serializer = StorySerializer(
            story,
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        story = self.get_object(pk)
        serializer = StorySerializer(
            story,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        story = self.get_object(pk)
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)