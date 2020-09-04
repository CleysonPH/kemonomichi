from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from appointments.models import Appointment


class AppointmentModelTest(TestCase):
    def test_pet_label(self):
        pet_label = Appointment._meta.get_field("pet").verbose_name
        self.assertEqual(pet_label, "Pet")

    def test_reason_label(self):
        reason_label = Appointment._meta.get_field("reason").verbose_name
        self.assertEqual(reason_label, "Motivo da Consulta")

    def test_reason_max_length(self):
        max_length = Appointment._meta.get_field("reason").max_length
        self.assertEqual(max_length, 200)

    def test_current_weight_label(self):
        current_weight_label = Appointment._meta.get_field(
            "current_weight"
        ).verbose_name
        self.assertEqual(current_weight_label, "Peso Atual")

    def test_current_drugs_label(self):
        current_drugs_label = Appointment._meta.get_field("current_drugs").verbose_name
        self.assertEqual(current_drugs_label, "Medicamento Atual")

    def test_prescribed_drugs_label(self):
        prescribed_drugs_label = Appointment._meta.get_field(
            "prescribed_drugs"
        ).verbose_name
        self.assertEqual(prescribed_drugs_label, "Medicamentos Prescritos")

    def test_prescribed_exams_label(self):
        prescribed_exams_label = Appointment._meta.get_field(
            "prescribed_exams"
        ).verbose_name
        self.assertEqual(prescribed_exams_label, "Exames Prescritos")

    def test_verbose_name(self):
        verbose_name = Appointment._meta.verbose_name
        self.assertEqual(verbose_name, "consulta")

    def test_verbose_name_plural(self):
        verbose_name_plural = Appointment._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "consultas")

    def test_string_representation(self):
        appointment = baker.make(Appointment)
        self.assertEqual(
            str(appointment), f"{appointment.pet.name} - {appointment.created_date}"
        )

    def test_get_absolute_url(self):
        appointment = baker.make(Appointment)
        self.assertEqual(
            appointment.get_absolute_url(),
            reverse("appointments:appointment-detail", kwargs={"pk": appointment.pk}),
        )
