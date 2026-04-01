"""class based views for DRF"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from source.models import Source
from source.serializers import SourceSerializer


class SourceListCreateAPIView(APIView):

    def get(self, request):
        sources = (
            Source.objects
            .select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies")
        )
        serializer = SourceSerializer(sources, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SourceSerializer(
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


class SourceDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(
            Source.objects
            .select_related("company", "created_by", "updated_by")
            .prefetch_related("tagged_companies"),
            pk=pk
        )

    def get(self, request, pk):
        source = self.get_object(pk)
        serializer = SourceSerializer(source)
        return Response(serializer.data)

    def put(self, request, pk):
        source = self.get_object(pk)
        serializer = SourceSerializer(
            source,
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        source = self.get_object(pk)
        serializer = SourceSerializer(
            source,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        source = self.get_object(pk)
        source.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)