from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()


# Регистрация пользователя
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


# Представление пользователя для получения и обновления данных
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# Обработчик создания токенов (JWT)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


# Выход из системы (черный список refresh токена)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Извлекаем refresh токен из запроса
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Требуется refresh-токен"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Создаем объект refresh токена и добавляем его в черный список
            token = RefreshToken(refresh_token)
            token.blacklist()  # Для этого нужен blacklisting

            return Response(
                {"message": "Вы вышли из системы"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Сериализатор для вывода и обновления данных пользователя
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
