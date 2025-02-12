from django.urls import path

from .views import (HabitCreateView, HabitDeleteView, HabitListView,
                    HabitUpdateView, PublicHabitsView, UserRegistrationView,
                    register_telegram)

urlpatterns = [
    path("habits/", HabitListView.as_view(), name="list-habits"),
    path("habits/create/", HabitCreateView.as_view(), name="create-habit"),
    path("habits/public/", PublicHabitsView.as_view(), name="public-habits"),
    path("habits/<int:pk>/update/", HabitUpdateView.as_view(), name="habit-update"),
    path("habits/<int:pk>/delete/", HabitDeleteView.as_view(), name="habit-delete"),
    path("users/register/", UserRegistrationView.as_view(), name="user-register"),
    path("telegram/register/", register_telegram, name="register_telegram"),
]
