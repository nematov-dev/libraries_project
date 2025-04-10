from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser

from app_auth.models import Library
from app_auth.serializers import LibrarySerializer
from app_books.serializers import BookSerializer
from app_books.paginations import BookPagination
from app_libraries.serializers import LibraryStatusSerializer


class LibraryListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        libraries = Library.objects.all()
        data = []

        for library in libraries:
            books_count = library.books.count()

            data.append({
                "id":library.id,
                "name": library.user.name,
                "image":library.image.url if library.image else None,
                "address":library.address,
                "total_books": books_count ,
                "is_active":library.user.is_active
            })

        return Response(data)

class LibraryDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            library = Library.objects.get(id=kwargs['pk'])
            
            books = library.books.all().order_by('id')

            # Pagination uchun
            paginator = BookPagination()
            result_books = paginator.paginate_queryset(books, request)

            # Serializatsiya
            library_data = LibrarySerializer(library).data
            books_data = BookSerializer(result_books, many=True).data

            # Natija
            return paginator.get_paginated_response({
                "library": library_data,
                "phone":library.user.phone,
                "is_active":library.user.is_active,
                "books": books_data,
                "total_books": books.count(),
            })

        except Library.DoesNotExist:
            return Response({"status":False,"detail": "Library not found."}, status=status.HTTP_404_NOT_FOUND)

    
class ActivateLibraryAPIView(APIView):
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(request_body=LibraryStatusSerializer)
    def patch(self, request, pk, *args, **kwargs):
        try:
            library = Library.objects.get(id=pk)
        except Library.DoesNotExist:
            return Response({"status":False,"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializerni yaratish va requestdan is_active qiymatini olish
        serializer = LibraryStatusSerializer(data=request.data)
        if serializer.is_valid():
            # is_active qiymatiga qarab faollashtirish yoki faollasizlantirish
            library.user.is_active = serializer.validated_data['is_active']
            library.user.save()

            return Response({"status": True, "detail": "Library deactivate successful."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeactivateLibraryAPIView(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, pk, *args, **kwargs):
        try:
            library = Library.objects.get(id=pk)
        except Library.DoesNotExist:
            return Response({"status":False,"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

        # Kutubxona profilini faolsizlantirish
        library.user.is_active = False
        library.user.save()

        return Response({"status":True,"detail": "Library deactivate successul."}, status=status.HTTP_200_OK)
    