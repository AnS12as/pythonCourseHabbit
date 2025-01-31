from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    """
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")

    def create(self, validated_data):
        """
        Создает нового пользователя с хешированным паролем.
        """
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone", ""),
            city=validated_data.get("city", ""),
            avatar=validated_data.get("avatar", None),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра и обновления профиля пользователя.
    """
    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar")
        read_only_fields = ("email",)
