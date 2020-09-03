from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy


class EmployeeListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/funcionarios/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("employees:employee-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("employees:employee-list"))
        self.assertTemplateUsed(response, "employees/employee_list.html")

    def test_page_title(self):
        response = self.client.get(reverse("employees:employee-list"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Lista de Funcionários")

    def test_list_all_clients(self):
        employees = mommy.make("employees.Employee", 10)
        response = self.client.get(reverse("employees:employee-list"))
        self.assertEqual(len(response.context["employees"]), 10)

        for employee in employees:
            self.assertTrue(employee in response.context["employees"])
