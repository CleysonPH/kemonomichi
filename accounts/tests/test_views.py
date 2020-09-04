from datetime import date
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee


class SigninViewTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "test_username",
            "password": "test_password",
        }

        self.wrong_credentials = {
            "username": "wrong_test_username",
            "password": "wrong_test_password",
        }

        self.user = Employee.objects.create_user(
            username=self.credentials["username"],
            password=self.credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/contas/login/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("accounts:signin"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("accounts:signin"))
        self.assertTemplateUsed(response, "adminlte/login.html")

    def test_login(self):
        response = self.client.post(
            reverse("accounts:signin"), self.credentials, follow=True
        )

        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"], self.user)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_redirects_to_dashboard_when_login_successfully(self):
        response = self.client.post(
            reverse("accounts:signin"), self.credentials, follow=True
        )

        self.assertRedirects(response, reverse("core:dashboard"))


class SiginoutViewTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "test_username",
            "password": "test_password",
        }
        self.user = Employee.objects.create_user(
            username=self.credentials["username"],
            password=self.credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.credentials)
        response = self.client.get(f"/contas/logout/")
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse("accounts:signout"))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse("accounts:signout"), follow=True)

        self.assertIn("user", response.context)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_redirects_to_sigin_when_logout_successfully(self):
        self.client.login(**self.credentials)
        response = self.client.post(reverse("accounts:signout"), follow=True)

        self.assertRedirects(response, reverse("accounts:signin"))
