from django.urls import path
from .views import HabitCreateView, HabitListView, PublicHabitsView, register_telegram

urlpatterns = [
    path("habits/", HabitListView.as_view(), name="list-habits"),
    path("habits/create/", HabitCreateView.as_view(), name="create-habit"),
    path("habits/public/", PublicHabitsView.as_view(), name="public-habits"),
    path("telegram/register/", register_telegram, name="register_telegram"),
]
