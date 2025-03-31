from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions


from .serializers import UserAndLibrarySerializer,UserSerializer,LibrarySerializer,LoginSerializer,LibraryProfileSerializer
from .models import Library

User = get_user_model()

class CreateLibraryAPIView(APIView):

    @swagger_auto_schema(request_body=UserAndLibrarySerializer)
    def post(self, request):
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save(is_librarian=True,is_active=False)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        library_data = request.data.get('library', {})   
        library_serializer = LibrarySerializer(data=library_data)

        if library_serializer.is_valid():
            phone = user_data.get('phone')
            user_l = User.objects.get(phone=phone)
            library_serializer.validated_data['user'] = user_l
            library_serializer.save()
            return Response(library_serializer.data, status=status.HTTP_201_CREATED)

        else:
            user.delete()
            return Response(library_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginAPIView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        user = User.objects.filter(phone=phone).first()

        if not user.is_active:
             return Response({"status":False,"detail": "Your account is not active."}, status=status.HTTP_401_UNAUTHORIZED)

        if user and user.check_password(password):

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        return Response({"status":False,"detail": "The phone number or password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Tokenni qora ro‘yxatga qo‘shish
            return Response({"status":True,"detail": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class LibraryProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Kutubxona profilini olish, agar bo‘lmasa, `None` qaytarish."""
        return Library.objects.first()

    def get(self, request):
        """Kutubxona profilini olish"""
        profile = self.get_object()
        if not profile:
            return Response({"status":False,"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LibraryProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=LibraryProfileSerializer)
    def patch(self, request):
        """Kutubxona profilini yangilash"""
        profile = self.get_object()
        if not profile:
            return Response({"status":False,"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LibraryProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

