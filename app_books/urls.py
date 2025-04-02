from django.urls import path


from .views import BookDetailAPIView,BookListCreateAPIView,SearchBooksAPIView,UploadExcelAPIView,AddBooksAPIView


urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('book/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('search/book/',SearchBooksAPIView.as_view(),name='search-book'),
    path('upload-excel/', UploadExcelAPIView.as_view(), name='upload-excel'),
    path('add-books/',AddBooksAPIView.as_view(),name='add-books')
]