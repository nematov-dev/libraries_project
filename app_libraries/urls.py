from django.urls import path

from app_libraries.views import LibraryListCreateAPIView,LibraryDetailAPIView,ActivateLibraryAPIView

urlpatterns = [
    path('libraries/', LibraryListCreateAPIView.as_view(), name='library-list-create'),
    path('library/<int:pk>/', LibraryDetailAPIView.as_view(), name='library-detail'),
    path('library/activate/<int:pk>/', ActivateLibraryAPIView.as_view(), name='library-activate'),
]