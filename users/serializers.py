from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ['email', 'password', 'username']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        """Проверка на уникальность email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован.")
        return value

    def create(self, validated_data):
        """Создание пользователя."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username', None)
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и обновления профиля пользователя."""

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar")
        read_only_fields = ("email",)
