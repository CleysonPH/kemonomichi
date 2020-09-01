from django.db import models
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
