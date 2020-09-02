from django.db import models
from django.urls import reverse
from django_localflavor_br.br_states import STATE_CHOICES


class Address(models.Model):
    street = models.CharField("Rua", max_length=50, null=False, blank=False)
    city = models.CharField("Cidade", max_length=30, null=False, blank=False)
    state = models.CharField(
        "Estado", max_length=2, choices=STATE_CHOICES, null=False, blank=False
    )

    class Meta:
        verbose_name = "endereço"
        verbose_name_plural = "endereços"

    def __str__(self):
        return f"{self.street}, {self.city} - {self.state}"


class Client(models.Model):
    name = models.CharField("Nome", max_length=100, null=False, blank=False)
    email = models.EmailField("Email", null=False, blank=False)
    address = models.ForeignKey(
        "clients.Address", verbose_name="Endereço", on_delete=models.CASCADE
    )
    cpf = models.CharField("CPF", max_length=14, null=False, blank=False)
    birth_date = models.DateField("Data de Nascimento", null=False, blank=False)
    occupation = models.CharField("Profissão", max_length=25, null=False, blank=False)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("clients:client-detail", kwargs={"pk": self.pk})
