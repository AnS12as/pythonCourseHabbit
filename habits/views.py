from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets

from .filters import HabitFilter
from .models import Habit
from .serializers import HabitSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
import json


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками (CRUD).

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


class HabitCreateView(APIView):
    """
        APIView для создания новой привычки.

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
    """
        APIView для получения списка привычек текущего пользователя.

        Метод:
            - get: Возвращает список привычек текущего пользователя.
        """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(habits, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class PublicHabitsView(APIView):
    """
        APIView для получения публичных привычек.

        Метод:
            - get: Возвращает список публичных привычек.
        """
    permission_classes = [AllowAny]

    def get(self, request):
        habits = Habit.objects.filter(is_public=True)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
def register_telegram(request):
    """
        Регистрация Telegram ID пользователя.

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
