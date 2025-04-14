from rest_framework import serializers


from .models import Book,Library
from app_auth.serializers import LibrarySerializer


class BookSerializer(serializers.ModelSerializer):
    library = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Book
        fields = ('id','library','name', 'author', 'publisher', 'quantity_in_library')

class BookSearchSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()
    class Meta:
        model = Book
        fields = ('id','name', 'author', 'publisher', 'quantity_in_library','library')
