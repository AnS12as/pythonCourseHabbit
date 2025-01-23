from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("action", "time", "user", "is_public")
    list_filter = ("is_public", "user")

