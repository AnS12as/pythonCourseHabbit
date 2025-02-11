from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Разрешает доступ к объекту только его владельцу для редактирования.

    Чтение разрешено всем аутентифицированным пользователям.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем (GET, HEAD, OPTIONS)
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        # Разрешаем изменение только владельцу объекта
        return obj == request.user


class IsAuthenticatedAndOwner(BasePermission):
    """Разрешает доступ только аутентифицированному пользователю и только к
    своим данным."""

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj == request.user
