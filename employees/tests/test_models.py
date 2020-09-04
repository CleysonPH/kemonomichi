from django.test import TestCase

from employees.models import Employee


class EmployeeModelTest(TestCase):
    def test_birth_date_label(self):
        birth_date_label = Employee._meta.get_field("birth_date").verbose_name
        self.assertEqual(birth_date_label, "Data de Nascimento")

    def test_role_label(self):
        role_label = Employee._meta.get_field("role").verbose_name
        self.assertEqual(role_label, "Cargo")

    def test_verbose_name(self):
        verbose_name = Employee._meta.verbose_name
        self.assertEqual(str(verbose_name), "funcionário")

    def test_verbose_name_plural(self):
        verbose_name_plural = Employee._meta.verbose_name_plural
        self.assertEqual(str(verbose_name_plural), "funcionários")
