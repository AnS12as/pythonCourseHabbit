from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ["id"]  # Sorting by id instead of username
    list_display = ["email", "phone", "city", "is_staff", "is_superuser"]
    search_fields = ["email", "phone"]

    # Adjusted fieldsets to reflect the fields in the custom User model
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("phone", "city", "avatar", "telegram_id")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Adjust add_fieldsets as well
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    # Remove references to `groups` and `user_permissions` from filter_horizontal and list_filter
    filter_horizontal = ()  # Empty tuple, as groups and user_permissions do not exist
    list_filter = ["is_staff", "is_superuser"]  # Adjust this list based on existing fields


admin.site.register(User, CustomUserAdmin)
