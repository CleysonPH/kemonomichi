from datetime import date
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from appointments.models import Appointment
from employees.models import Employee


class AppointmentCreateViewTest(TestCase):
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
        self.pet = baker.make("pets.Pet")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(f"/consultas/cadastrar/{self.pet.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-create", args=[self.pet.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-create", args=[self.pet.pk])
        )
        self.assertTemplateUsed(response, "appointments/appointment_form.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-create", args=[self.pet.pk])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Cadastrar Consulta")

    def test_redirects_to_pet_detail_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("appointments:appointment-create", args=[self.pet.pk]),
            {
                "reason": "Dor na pata dianteira esquerda",
                "current_weight": 10.5,
                "current_drugs": "",
                "prescribed_drugs": "",
                "prescribed_exams": "",
            },
        )

        self.assertRedirects(response, self.pet.get_absolute_url())

    def test_create_pet_in_database_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        appointment_data = {
            "reason": "Dor na pata dianteira esquerda",
            "current_weight": 10.5,
            "current_drugs": "",
            "prescribed_drugs": "",
            "prescribed_exams": "",
        }
        response = self.client.post(
            reverse("appointments:appointment-create", args=[self.pet.pk]),
            appointment_data,
        )

        appointment = Appointment.objects.get(reason=appointment_data["reason"])

        self.assertEqual(appointment_data["reason"], appointment.reason)
        self.assertEqual(appointment_data["current_weight"], appointment.current_weight)
        self.assertEqual(appointment_data["current_drugs"], appointment.current_drugs)
        self.assertEqual(
            appointment_data["prescribed_drugs"], appointment.prescribed_drugs
        )
        self.assertEqual(
            appointment_data["prescribed_exams"], appointment.prescribed_exams
        )

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("appointments:appointment-create", args=[self.pet.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))

    def test_redirect_to_signin_when_have_the_role_financeiro(self):
        financeiro_credentials = {
            "username": "financeiro_test_username",
            "password": "financeiro_test_password",
        }
        financeiro_user = Employee.objects.create_user(
            username=financeiro_credentials["username"],
            password=financeiro_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=3,
        )
        self.client.login(**financeiro_credentials)
        url = reverse("appointments:appointment-create", args=[self.pet.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))

    def test_redirect_to_signin_when_have_the_role_atendimento(self):
        atendimento_credentials = {
            "username": "atendimento_test_username",
            "password": "atendimento_test_password",
        }
        atendimento_user = Employee.objects.create_user(
            username=atendimento_credentials["username"],
            password=atendimento_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=4,
        )
        self.client.login(**atendimento_credentials)
        url = reverse("appointments:appointment-create", args=[self.pet.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class AppointmentDetailViewTest(TestCase):
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
        self.appointment = baker.make("appointments.Appointment")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(f"/consultas/{self.appointment.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-detail", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-detail", args=[self.appointment.pk])
        )
        self.assertTemplateUsed(response, "appointments/appointment_detail.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-detail", args=[self.appointment.pk])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Detalhes da Consulta")

    def test_show_correct_appointment(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-detail", args=[self.appointment.pk])
        )
        self.assertIn("appointment", response.context)
        self.assertEqual(response.context["appointment"], self.appointment)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("appointments:appointment-detail", args=[self.appointment.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class AppointmentListViewTest(TestCase):
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
        response = self.client.get("/consultas/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("appointments:appointment-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("appointments:appointment-list"))
        self.assertTemplateUsed(response, "appointments/appointment_list.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("appointments:appointment-list"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Lista de Consultas")

    def test_list_all_appointments(self):
        self.client.login(**self.admin_credentials)
        appointments = baker.make("appointments.Appointment", 10)
        response = self.client.get(reverse("appointments:appointment-list"))
        self.assertEqual(len(response.context["appointments"]), 10)

        for appointment in appointments:
            self.assertTrue(appointment in response.context["appointments"])

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("appointments:appointment-list")
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class AppointmentDeleteViewTest(TestCase):
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
        self.appointment_data = baker.make("appointments.Appointment")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(f"/consultas/{self.appointment_data.pk}/remover/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-delete", args=[self.appointment_data.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-delete", args=[self.appointment_data.pk])
        )
        self.assertTemplateUsed(
            response, "appointments/appointments_delete_confirm.html"
        )

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-delete", args=[self.appointment_data.pk])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Remover Consulta")

    def test_show_correct_appointment(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("appointments:appointment-delete", args=[self.appointment_data.pk])
        )
        self.assertIn("appointment", response.context)
        self.assertEqual(response.context["appointment"], self.appointment_data)

    def test_redirects_to_appointment_list_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("appointments:appointment-delete", args=[self.appointment_data.pk])
        )

        self.assertRedirects(response, reverse("appointments:appointment-list"))

    def test_delete_appointment_in_database_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("appointments:appointment-delete", args=[self.appointment_data.pk]),
        )

        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(pk=1)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse(
            "appointments:appointment-delete", args=[self.appointment_data.pk]
        )
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))

    def test_redirect_to_signin_when_have_the_role_financeiro(self):
        financeiro_credentials = {
            "username": "financeiro_test_username",
            "password": "financeiro_test_password",
        }
        financeiro_user = Employee.objects.create_user(
            username=financeiro_credentials["username"],
            password=financeiro_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=3,
        )
        self.client.login(**financeiro_credentials)
        url = reverse(
            "appointments:appointment-delete", args=[self.appointment_data.pk]
        )
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))

    def test_redirect_to_signin_when_have_the_role_atendimento(self):
        atendimento_credentials = {
            "username": "atendimento_test_username",
            "password": "atendimento_test_password",
        }
        atendimento_user = Employee.objects.create_user(
            username=atendimento_credentials["username"],
            password=atendimento_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=4,
        )
        self.client.login(**atendimento_credentials)
        url = reverse(
            "appointments:appointment-delete", args=[self.appointment_data.pk]
        )
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))
