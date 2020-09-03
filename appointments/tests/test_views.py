from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from appointments.models import Appointment


class AppointmentCreateViewTest(TestCase):
    def setUp(self):
        self.pet = mommy.make("pets.Pet")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/consultas/cadastrar/{self.pet.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("appointments:appointment-create", args=[self.pet.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("appointments:appointment-create", args=[self.pet.pk])
        )
        self.assertTemplateUsed(response, "appointments/appointment_form.html")

    def test_page_title(self):
        response = self.client.get(
            reverse("appointments:appointment-create", args=[self.pet.pk])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Cadastrar Consulta")

    def test_redirects_to_pet_detail_after_submit_form_with_success(self):
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
