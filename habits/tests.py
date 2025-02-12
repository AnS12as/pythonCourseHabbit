from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from django.test import TestCase
from habits.models import Habit


class HabitAPITest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        # Generate JWT token
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Define URLs for the API endpoints
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
        """Test habit creation with invalid data."""
        data = {
            "place": "Park",
            "time": "08:00:00",
            "action": "Morning jog",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Smoothie",
            "duration": 150,  # Invalid duration (more than 120 minutes)
            "is_public": True,
        }
        response = self.client.post(self.habit_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Ensure this value is less than or equal to 120.", str(response.data)
        )

    def test_create_habit_missing_action(self):
        """Test habit creation with missing required field (action)."""
        data = {
            "place": "Park",
            "time": "08:00:00",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Smoothie",
            "duration": 30,
            "is_public": True,
        }
        response = self.client.post(self.habit_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", str(response.data))

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

    def test_public_habits_no_access_to_private(self):
        """Test if user can't see private habits on public endpoint."""
        Habit.objects.create(
            user=self.user,
            place="Park",
            time="08:00:00",
            action="Morning jog",
            duration=30,
            is_public=False,
        )
        response = self.client.get(self.public_habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_habit_no_authentication(self):
        """Test for habit creation without authentication."""
        self.client.credentials()  # Clear authentication credentials
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRegistrationTest(TestCase):
    def test_register_user_success(self):
        data = {
            "email": "newuser@example.com",
            "password": "testpass123",
        }
        response = self.client.post(reverse("user-register"), data)

        # Check that the user was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "newuser@example.com")

    def test_register_user_existing_email(self):
        User.objects.create_user(email="newuser@example.com", password="testpass123", username="newuser")
        data = {
            "email": "newuser@example.com",
            "password": "testpass123",
            "username": "newuser2",  # Add new username
        }
        response = self.client.post(reverse("user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", str(response.data))  # Adjust this line to expect the field name for duplicates

    def test_register_user_invalid_email_format(self):
        data = {
            "email": "invalidemail",
            "password": "testpass123",
            "username": "invaliduser",  # Add username
        }
        response = self.client.post(reverse("user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address.", str(response.data))

    def test_register_user_missing_email(self):
        data = {
            "password": "testpass123",
            "username": "userwithoutemail",  # Add username
        }
        response = self.client.post(reverse("user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", str(response.data))

    def test_register_user_missing_password(self):
        data = {
            "email": "newuser@example.com",
            "username": "userwithoutpassword",  # Add username
        }
        response = self.client.post(reverse("user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", str(response.data))
