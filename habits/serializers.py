from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(
        max_value=120,
        error_messages={"max_value": "Duration cannot exceed 120 seconds."},
    )
    """Сериализатор для работы с моделью Habit.

    Поля:
        - id: Уникальный идентификатор.
        - user: Владелец привычки (только для чтения).
        - place, time, action: Информация о привычке.
        - is_pleasant, frequency, reward, duration, is_public: Детали привычки.
    """

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "frequency",
            "reward",
            "duration",
            "is_public",
        ]
        read_only_fields = ["user"]

    def validate(self, data):
        """Проверка данных для привычки."""
        # Проверка длительности привычки
        if data.get("duration", 0) > 120:
            raise serializers.ValidationError("Duration cannot exceed 120 seconds.")

        # Проверка на одновременное указание награды и связанной привычки
        if data.get("reward") and data.get("linked_habit"):
            raise serializers.ValidationError(
                "Either reward or linked habit must be set, not both."
            )

        # Приятная привычка не может иметь награду или связанную привычку
        if data.get("is_pleasant") and (data.get("reward") or data.get("linked_habit")):
            raise serializers.ValidationError(
                "Pleasant habits cannot have a reward or linked habit."
            )

        # Проверка частоты выполнения привычки от 1 до 7 дней
        frequency = data.get("frequency")
        if frequency is not None and (frequency < 1 or frequency > 7):
            raise serializers.ValidationError("Frequency must be between 1 and 7 days.")

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "phone",
            "city",
            "avatar",
        )  # Убедись, что эти поля существуют в модели

    def create(self, validated_data):
        """Создаёт нового пользователя с хешированным паролем."""
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get(
                "phone", ""
            ),  # Проверь, что такие поля существуют в модели
            city=validated_data.get("city", ""),
            avatar=validated_data.get("avatar", None),
        )
        return user
