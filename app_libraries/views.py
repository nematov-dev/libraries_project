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


class LibraryListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        libraries = Library.objects.all()
        data = []

        for library in libraries:
            books_count = library.books.aggregate(total=Sum('quantity_in_library'))['total'] or 0

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

    def delete(self, request, pk):
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.is_staff:
                try:
                    library = Library.objects.get(pk=pk)
                except Library.DoesNotExist:
                    return Response({"status":False,"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

                library.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response({"status":False,"detail":"This is for admins only"})
        return Response({"status":False,"detail":"Not authenticated"})
    
class ActivateLibraryAPIView(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, pk, *args, **kwargs):
        try:
            library = Library.objects.get(id=pk)
        except Library.DoesNotExist:
            return Response({"status":False,"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

        # Kutubxona profilini faollashtirish (aktiv qilish)
        library.user.is_active = True
        library.user.save()

        return Response({"status":True,"detail": "Library activate successul."}, status=status.HTTP_200_OK)
