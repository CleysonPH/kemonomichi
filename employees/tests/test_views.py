from datetime import date
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from employees.models import Employee


class EmployeeListViewTest(TestCase):
    def setUp(self):
        self.admin_credentials = {
            "username": "admin_test_username",
            "password": "admin_test_password",
        }
        self.admin_user = Employee.objects.create_user(
            username=self.admin_credentials["username"],
            password=self.admin_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get("/funcionarios/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("employees:employee-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("employees:employee-list"))
        self.assertTemplateUsed(response, "employees/employee_list.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("employees:employee-list"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Lista de Funcionários")

    def test_list_all_clients(self):
        self.client.login(**self.admin_credentials)
        employees = baker.make("employees.Employee", 9)
        response = self.client.get(reverse("employees:employee-list"))
        self.assertEqual(len(response.context["employees"]), 10)

        for employee in employees:
            self.assertTrue(employee in response.context["employees"])

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("employees:employee-list")
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))
