from rest_framework import serializers

from app_auth.models import Library

class LibraryStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
