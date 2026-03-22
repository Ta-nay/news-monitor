
from rest_framework import serializers
from source.models import Source

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "name", "url"]