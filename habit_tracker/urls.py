from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="Документация API для Habit Tracker",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Открываем Swagger для всех
    permission_classes=[AllowAny],  # Убираем авторизацию
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("habits.urls")),
    path("api/users/", include("users.urls")),

    # Эндпоинты для токенов
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger и Redoc документация
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
]