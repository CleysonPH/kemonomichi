from django.db import models


class Pet(models.Model):
    SPECIE_CHOICES = (
        ("CA", "Cachorro"),
        ("GA", "Gato"),
        ("CO", "Coelho"),
    )

    COLOR_CHOICES = (
        ("PR", "Preto"),
        ("BR", "Branco"),
        ("CI", "Cinza"),
        ("MA", "Marrom"),
    )

    name = models.CharField("Nome", max_length=50, null=False, blank=False)
    birth_date = models.DateField("Data de Nascimento", null=False, blank=False)
    specie = models.CharField(
        "Espécie", max_length=2, choices=SPECIE_CHOICES, null=False, blank=False
    )
    color = models.CharField(
        "Cor", max_length=2, choices=COLOR_CHOICES, null=False, blank=False
    )
    owner = models.ForeignKey(
        "clients.Client",
        verbose_name="Dono",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "pet"
        verbose_name_plural = "pets"

    def __str__(self):
        return self.name
