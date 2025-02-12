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


class UserRegistrationTest(TestCase):
    def test_register_user_success(self):
        data = {
            "email": "newuser@example.com",
            "password": "testpass123",
        }

    def test_register_user_existing_email(self):
        User.objects.create_user(email="newuser@example.com", password="testpass123")
        data = {
            "email": "newuser@example.com",
            "password": "testpass123",
        }

    def test_register_user_invalid_email_format(self):
        data = {
            "email": "invalidemail",
            "password": "testpass123",
        }

    def test_register_user_missing_email(self):
        data = {
            "password": "testpass123",
        }

    def test_register_user_missing_password(self):
        data = {
            "email": "newuser@example.com",
        }
