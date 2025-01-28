from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from django.urls import reverse
from habits.models import Habit


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.habit_create_url = reverse("create-habit")
        self.habit_list_url = reverse("list-habits")
        self.public_habits_url = reverse("public-habits")

    def test_create_habit_success(self):
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
        """Тест создания привычки с невалидными данными"""
        data = {
            "place": "Park",
            "time": "08:00:00",
            "action": "Morning jog",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Smoothie",
            "duration": 150,
            "is_public": True,
        }
        response = self.client.post(self.habit_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Duration cannot exceed 120 seconds.", str(response.data))

    def test_list_habits(self):
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
        data = {"username": "newuser", "email": "newuser@example.com", "password": "testpass123"}
        response = self.client.post(reverse("user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "newuser")

    def test_register_user_existing_username(self):
        User.objects.create_user(username="newuser", email="newuser@example.com", password="testpass123")
        data = {"username": "newuser", "email": "anotheremail@example.com", "password": "testpass123"}
        response = self.client.post(reverse("user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username already exists", str(response.data))
