from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Habit
from django.contrib.auth.models import Group

User = get_user_model()


class HabitTests(APITestCase):
    def setUp(self):
        self.api_client = APIClient()
        # Создание пользователей
        self.owner = User.objects.create_user(email="owner@example.com", password="password")
        self.moderator_user = User.objects.create_user(email="moderator@example.com", password="password")
        self.regular_user = User.objects.create_user(email="user@example.com", password="password")

        # Добавляем модератора в группу
        moderator_group, _ = Group.objects.get_or_create(name="Moderators")
        self.moderator_user.groups.add(moderator_group)

        # Создание привычки
        self.habit = Habit.objects.create(
            user=self.owner,
            place="Park",
            time="08:00:00",
            action="Morning jog",
            is_pleasant=False,
            frequency=1,
            reward="Smoothie",
            duration=30,
            is_public=True,
        )

    def test_create_habit_success(self):
        self.api_client.force_authenticate(user=self.owner)
        data = {
            "place": "Gym",
            "time": "06:00:00",
            "action": "Morning workout",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Protein shake",
            "duration": 30,
            "is_public": True,
        }
        response = self.api_client.post("/habits/habits/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_habit_invalid_duration(self):
        self.api_client.force_authenticate(user=self.owner)
        data = {
            "place": "Gym",
            "time": "06:00:00",
            "action": "Morning workout",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Protein shake",
            "duration": 150,  # Invalid duration
            "is_public": True,
        }
        response = self.api_client.post("/habits/habits/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Duration cannot exceed 120 seconds.", str(response.data))

    def test_update_habit_as_owner(self):
        self.api_client.force_authenticate(user=self.owner)
        data = {"action": "Updated Morning jog"}
        response = self.api_client.patch(f"/habits/habits/{self.habit.id}/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Updated Morning jog")

    def test_delete_habit_as_owner(self):
        self.api_client.force_authenticate(user=self.owner)
        response = self.api_client.delete(f"/habits/habits/{self.habit.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверим, что привычка была удалена
        with self.assertRaises(Habit.DoesNotExist):
            Habit.objects.get(id=self.habit.id)

    def test_delete_habit_as_moderator(self):
        self.api_client.force_authenticate(user=self.moderator_user)
        response = self.api_client.delete(f"/habits/habits/{self.habit.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscription_add_remove(self):
        self.api_client.force_authenticate(user=self.owner)
        # Проверяем добавление подписки
        response = self.api_client.post("/habits/subscriptions/", {"habit_id": self.habit.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Subscription added")

        # Проверяем удаление подписки
        response = self.api_client.post("/habits/subscriptions/", {"habit_id": self.habit.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Subscription removed")
