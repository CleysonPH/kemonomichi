from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

from core.models import BaseModel


class Appointment(BaseModel):
    pet = models.ForeignKey(
        "pets.Pet",
        verbose_name="Pet",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    reason = models.CharField(
        "Motivo da Consulta", max_length=200, null=False, blank=False
    )
    current_weight = models.FloatField("Peso Atual", null=False, blank=False)
    current_drugs = models.TextField("Medicamento Atual", null=False, blank=True)
    prescribed_drugs = models.TextField(
        "Medicamentos Prescritos", null=False, blank=True
    )
    prescribed_exams = models.TextField("Exames Prescritos", null=False, blank=True)

    class Meta:
        verbose_name = "consulta"
        verbose_name_plural = "consultas"
        ordering = ("-created_date",)

    def __str__(self):
        return f"{self.pet.name} - {self.created_date}"

    def get_absolute_url(self):
        return reverse("appointments:appointment-detail", kwargs={"pk": self.pk})

    def send_mail(self):
        subject = "Resumo da consulta"
        message = "Resumo da sua consulta"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.pet.owner.email]
        html_message = render_to_string(
            "appointments/appointment_mail.html", {"appointment": self}
        )
        send_mail(
            subject, message, from_email, recipient_list, html_message=html_message
        )
