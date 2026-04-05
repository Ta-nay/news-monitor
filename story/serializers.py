from rest_framework import serializers
from .models import Story
from company.models import Company
from source.models import Source


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class SourceSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "name"]


class StorySerializer(serializers.ModelSerializer):
    # READ
    company = CompanySerializer(read_only=True)
    source = SourceSimpleSerializer(read_only=True)
    tagged_companies = CompanySerializer(many=True, read_only=True)

    # WRITE (IDs)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source="company",
        write_only=True
    )
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Source.objects.all(),
        source="source",
        write_only=True
    )
    tagged_company_ids = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        many=True,
        source="tagged_companies",
        write_only=True
    )

    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "body_text",
            "url",

            "company",
            "company_id",

            "source",
            "source_id",

            "tagged_companies",
            "tagged_company_ids",

            "created_by",
            "updated_by",
            "created_on",
            "updated_on",
        ]

        read_only_fields = [
            "created_by",
            "updated_by",
            "created_on",
            "updated_on",
        ]