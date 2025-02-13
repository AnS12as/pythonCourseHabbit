from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """
    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "telegram_id"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "phone", "city", "avatar", "telegram_id"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
