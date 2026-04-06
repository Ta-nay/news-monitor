from rest_framework import serializers
from .models import Source
from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class SourceSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    tagged_companies = CompanySerializer(many=True, read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source="company",
        write_only=True
    )
    tagged_company_ids = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        many=True,
        source="tagged_companies",
        write_only=True
    )

    class Meta:
        model = Source
        fields = [
            "id",
            "name",
            "url",
            "company",              # read
            "company_id",           # write
            "tagged_companies",     # read
            "tagged_company_ids",   # write
            "created_by",
            "updated_by",
            "created_on",
            "updated_on",
        ]
        read_only_fields = ["created_by", "updated_by", "created_on", "updated_on"]

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return obj.created_by_id == request.user.id