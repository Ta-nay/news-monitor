"""function based views for DRF"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from source.models import Source
from source.serializers import SourceSerializer


@api_view(["GET", "POST"])
def source_list_create(request):
    if request.method == "GET":
        sources = (
            Source.objects
            .select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )
        serializer = SourceSerializer(sources, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = SourceSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                updated_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def source_detail(request, pk):
    source = get_object_or_404(
        Source.objects
        .select_related("company", "created_by", "updated_by")
        .prefetch_related("tagged_companies"),
        pk=pk
    )

    if request.method == "GET":
        serializer = SourceSerializer(source)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = SourceSerializer(
            source,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        source.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
