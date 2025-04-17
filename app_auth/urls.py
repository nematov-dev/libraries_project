from django.urls import path

from .views import CreateLibraryAPIView,LoginAPIView,LogoutView,LibraryProfileAPIView,AdminProfileAPIView

urlpatterns = [
    path('register-library/',CreateLibraryAPIView.as_view(),name='register-library'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',LibraryProfileAPIView.as_view(),name='profile'),
    path('admin/profile/',AdminProfileAPIView.as_view(),name='admin-profile')
]