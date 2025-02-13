from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterUserView(CreateAPIView):
    """
    Регистрация нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(ModelViewSet):
    """
    ViewSet для работы с пользователями (CRUD).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Вход пользователя с получением JWT токена.
    """
    permission_classes = [AllowAny]


class UserProfileView(APIView):
    """
    Просмотр профиля текущего пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Выход пользователя из системы.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
