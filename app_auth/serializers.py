from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Library

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone","password")

class LibraryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
        read_only_fields = ['created', 'updated','user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","password","name","phone")
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class LibrarySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    google_maps_url = serializers.SerializerMethodField()
    class Meta:
        model = Library
        fields = ('id','user','image','address','social_media','can_rent_books','latitude', 'longitude','google_maps_url')

    def get_google_maps_url(self, obj):
        if obj.latitude and obj.longitude:
            return f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
        return None

class UserAndLibrarySerializer(serializers.Serializer):
    user = UserSerializer()
    library = LibrarySerializer()
    