from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделью Habit.

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
        """
        Проверка данных для привычки:
        - Длительность не должна превышать 120 секунд.
        - Либо указана награда, либо связанная привычка, но не оба одновременно.
        - Приятная привычка не может иметь награду или связанную привычку.
        - Частота выполнения от 1 до 7 дней.
        """
        if data.get("duration", 0) > 120:
            raise serializers.ValidationError("Duration cannot exceed 120 seconds.")
        if data.get("reward") and data.get("linked_habit"):
            raise serializers.ValidationError(
                "Either reward or linked habit must be set, not both."
            )
        if data.get("is_pleasant") and (data.get("reward") or data.get("linked_habit")):
            raise serializers.ValidationError(
                "Pleasant habits cannot have a reward or linked habit."
            )
        if data.get("frequency", 1) < 1 or data.get("frequency") > 7:
            raise serializers.ValidationError("Frequency must be between 1 and 7 days.")
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователей.

    Поля:
        - username: Имя пользователя.
        - email: Электронная почта.
        - password: Пароль (только для записи).
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        """
        Создание нового пользователя с захешированным паролем.
        """
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
