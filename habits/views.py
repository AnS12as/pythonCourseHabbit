import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import HabitFilter
from .models import Habit
from .serializers import HabitSerializer, UserRegistrationSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками (CRUD).

    Методы:
        - get_queryset: Возвращает привычки текущего пользователя.
        - perform_create: Создает новую привычку, связывая её с текущим пользователем.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HabitFilter

    def get_queryset(self):
        """Получить все привычки текущего пользователя."""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Сохранить привычку для текущего пользователя."""
        serializer.save(user=self.request.user)


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    queryset = Habit.objects.filter(is_public=True)


class HabitCreateView(APIView):
    """APIView для создания новой привычки.

    Метод:
        - post: Сохраняет новую привычку, привязывая её к текущему пользователю.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HabitListView(APIView):
    """APIView для получения списка привычек текущего пользователя.

    Метод:
        - get: Возвращает список привычек текущего пользователя.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(habits, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class HabitUpdateView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitDeleteView(DestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user)


class PublicHabitsView(APIView):
    """APIView для получения публичных привычек.

    Метод:
        - get: Возвращает список публичных привычек.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        habits = Habit.objects.filter(is_public=True)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password, email=email)
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )


class UserRegistrationView(APIView):
    """
    post:
    Регистрация нового пользователя.

    Тело запроса:
        - username: Имя пользователя для нового аккаунта.
        - email: Электронная почта для нового аккаунта.
        - password: Пароль для нового аккаунта.

    Ответы:
        201: Пользователь успешно зарегистрирован.
        400: Ошибки валидации.
    """

    permission_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def register_telegram(request):
    """Регистрация Telegram ID пользователя.

    Принимает:
        - POST запрос с параметром `telegram_id`.

    Возвращает:
        - Успешное сообщение, если регистрация прошла успешно.
        - Ошибку, если токен невалиден или запрос некорректен.
    """
    if request.method == "POST":
        authenticator = JWTAuthentication()
        try:
            user, token = authenticator.authenticate(request)
            if not user:
                raise Exception("User not authenticated")
        except Exception as e:
            return JsonResponse(
                {"error": "Token authentication failed", "details": str(e)}, status=401
            )

        try:
            data = json.loads(request.body)
            telegram_id = data.get("telegram_id")
            if not telegram_id:
                return JsonResponse({"error": "telegram_id is required"}, status=400)

            profile = user.profile
            profile.telegram_id = telegram_id
            profile.save()

            return JsonResponse(
                {"message": "Telegram ID registered successfully"}, status=200
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
