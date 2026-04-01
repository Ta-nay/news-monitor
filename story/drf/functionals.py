"""function based views"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from story.models import Story
from story.serializers import StorySerializer




class StoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
def story_list_create(request):
    if request.method == "GET":
        stories = (
            Story.objects
            .select_related("company", "source", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )

        # 🔹 Apply pagination
        paginator = StoryPagination()
        page = paginator.paginate_queryset(stories, request)

        if page is not None:
            serializer = StorySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # fallback (rare)
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
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

from django.shortcuts import get_object_or_404


@api_view(["GET", "PUT", "PATCH", "DELETE"])
# @permission_classes([IsAuthenticated])
def story_detail(request, pk):
    stories = stories.filter(company=request.user.company)
    story = get_object_or_404(
        Story.objects
        .select_related("company", "source", "created_by", "updated_by")
        .prefetch_related("tagged_companies"),
        pk=pk
    )

    if request.method == "GET":
        serializer = StorySerializer(story)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = StorySerializer(
            story,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)