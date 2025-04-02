# books/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

from .models import Book,Library
from .serializers import BookSerializer,LibrarySearchSerializer


class BookListCreateAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=BookSerializer)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"status":False,"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)
        
    @swagger_auto_schema(request_body=BookSerializer)
    def put(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"status":False,"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"status":False,"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchBooksAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'q',  # Parametr nomi
                openapi.IN_QUERY,  # Query orqali yuboriladi
                description="Kitob nomi yoki muallifi bo‘yicha qidirish",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"status":False,"detail": "No search query entered"}, status=status.HTTP_400_BAD_REQUEST)

        # Kitob nomi yoki muallif bo‘yicha qidirish
        books = Book.objects.filter(Q(name__icontains=query) | Q(author__icontains=query))

        # Kitob joylashgan kutubxonalarni topish
        library_ids = books.values_list('library', flat=True).distinct()
        libraries = Library.objects.filter(id__in=library_ids)

        data = LibrarySearchSerializer(libraries, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
class UploadExcelAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        operation_description="Excel fayl yuklash va kitoblarni JSON formatida qaytarish",
        manual_parameters=[
            openapi.Parameter(
                "file",
                openapi.IN_FORM,
                description="Yuklanadigan Excel fayl (.xlsx, .xls)",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                "Yuklangan kitoblar ro‘yxati",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "books": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "author": openapi.Schema(type=openapi.TYPE_STRING),
                                    "publisher": openapi.Schema(type=openapi.TYPE_STRING),
                                    "quantity_in_library": openapi.Schema(type=openapi.TYPE_INTEGER)
                                }
                            )
                        )
                    }
                )
            ),
            400: "Xatolik yuz berdi"
        }
    )

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"status":False,"detail": "File failed to load"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)  # Excel faylni o‘qish
            books = df.to_dict(orient='records')  # Listga o‘tkazish
            return Response({"books": books}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AddBooksAPIView(APIView):
    @swagger_auto_schema(request_body=BookSerializer)
    def post(self, request, *args, **kwargs):
        books = request.data.get('books', [])

        if not books:
            return Response({"status":False,"detail": "The list of books is empty"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookSerializer(data=books, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":False,"detail": "Books saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)