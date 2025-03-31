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
        fields = ("id","password","full_name","phone")
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class LibrarySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Library
        fields = ('id','user','name','image','address','social_media','can_rent_books')

class UserAndLibrarySerializer(serializers.Serializer):
    user = UserSerializer()
    library = LibrarySerializer()
    