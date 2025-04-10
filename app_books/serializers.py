from rest_framework import serializers


from .models import Book,Library


class BookSerializer(serializers.ModelSerializer):
    library = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Book
        fields = ('id','library','name', 'author', 'publisher', 'quantity_in_library')

class LibrarySearchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name',read_only=True)
    class Meta:
        model = Library
        fields = ('id','name','address')