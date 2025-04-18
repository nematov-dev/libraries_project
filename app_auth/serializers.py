from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Library

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone","password")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","password","name","phone")
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","name","phone")

class LibraryProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Library
        fields = '__all__'
        read_only_fields = ['created', 'updated']
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        # Update Library fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related User fields
        if user_data:
            user = instance.user  # Bog'langan user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        return instance
    
    
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
    