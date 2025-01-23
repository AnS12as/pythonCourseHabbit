from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from habits.models import Habit


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.habit_create_url = "/api/habits/create/"
        self.habit_list_url = "/api/habits/"
        self.public_habits_url = "/api/habits/public/"

    def test_create_habit(self):
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
