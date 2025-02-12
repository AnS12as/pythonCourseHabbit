from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from habits.models import Habit


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # URL'ы для тестов
        self.habit_create_url = reverse("create-habit")
        self.habit_list_url = reverse("list-habits")
        self.public_habits_url = reverse("public-habits")

    def test_create_habit_success(self):
        """Тест на успешное создание привычки"""
        data = {
            "place": "Park",
            "time": "08:00:00",
            "action": "Morning jog",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Smoothie",
            "duration": 30,
            "is_public": True,
        }
        response = self.client.post(self.habit_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().action, "Morning jog")

    def test_create_habit_invalid_data(self):
        """Тест на создание привычки с невалидными данными"""
        data = {
            "place": "Park",
            "time": "08:00:00",
            "action": "Morning jog",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Smoothie",
            "duration": 150,  # Invalid duration
            "is_public": True,
        }
        response = self.client.post(self.habit_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Duration cannot exceed 120 seconds.", str(response.data))

    def test_create_habit_with_linked_habit_and_reward(self):
        """Тест на создание привычки с одновременным указанием связанной привычки и награды"""
        data = {
            "place": "Park",
            "time": "08:00:00",
            "action": "Morning jog",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Smoothie",
            "duration": 30,
            "is_public": True,
            "linked_habit": 1,  # Привязанная привычка
        }
        response = self.client.post(self.habit_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Можно задать либо награду, либо связанную привычку, но не обе одновременно.", str(response.data))

    def test_list_habits(self):
        """Тестирование получения списка привычек"""
        Habit.objects.create(
            user=self.user,
            place="Park",
            time="08:00:00",
            action="Morning jog",
            duration=30,
            is_public=False,
        )
        response = self.client.get(self.habit_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Morning jog")

    def test_public_habits(self):
        """Тестирование получения публичных привычек"""
        Habit.objects.create(
            user=self.user,
            place="Park",
            time="08:00:00",
            action="Morning jog",
            duration=30,
            is_public=True,
        )
        response = self.client.get(self.public_habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["action"], "Morning jog")


class UserRegistrationTest(APITestCase):

    def test_register_user_success(self):
        """Тест на успешную регистрацию пользователя"""
        data = {
            "email": "newuser@example.com",
            "password": "testpass123",
        }
        response = self.client.post(reverse("user-register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.first().email, "newuser@example.com")

    def test_register_user_existing_email(self):
        """Тест на попытку регистрации с уже существующим email"""
        get_user_model().objects.create_user(
            email="newuser@example.com", password="testpass123"
        )
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(reverse("user-register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email already exists", str(response.data))
