from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.credentials = {
            "username": "alice",
            "password": "A-long-test-password-872!",
        }

    def test_register_login_and_profile(self):
        response = self.client.post(reverse("users:register"), {
            **self.credentials, "email": "alice@example.com", "phone": "1234567890",
        })
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)
        user = get_user_model().objects.get(username="alice")
        self.assertTrue(user.check_password(self.credentials["password"]))
        response = self.client.post(reverse("users:login"), self.credentials)
        self.assertEqual(response.status_code, 200)
        access, refresh = response.data["access"], response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "alice")
        self.assertNotIn("password", response.data)
        self.client.credentials()
        response = self.client.post(reverse("users:refresh"), {"refresh": refresh})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_profile_requires_authentication(self):
        self.assertEqual(self.client.get(reverse("users:profile")).status_code, 401)

    def test_invalid_credentials(self):
        self.assertEqual(self.client.post(reverse("users:login"), self.credentials).status_code, 401)

    def test_weak_password_rejected(self):
        response = self.client.post(reverse("users:register"), {
            "username": "alice", "email": "alice@example.com", "password": "123",
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(get_user_model().objects.exists())

    def test_duplicate_email_rejected(self):
        get_user_model().objects.create_user(**self.credentials, email="alice@example.com")
        response = self.client.post(reverse("users:register"), {
            "username": "bob", "email": "alice@example.com",
            "password": self.credentials["password"],
        })
        self.assertEqual(response.status_code, 400)
