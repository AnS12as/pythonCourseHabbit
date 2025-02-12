from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return hasattr(obj, "id") and obj == request.user


class IsAuthenticatedAndOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(obj, "id")
            and obj == request.user
        )
