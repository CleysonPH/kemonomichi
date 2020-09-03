from django.db import models


class Appointment(models.Model):
    pet = models.ForeignKey(
        "pets.Pet",
        verbose_name="Pet",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    date = models.DateField("Data da Consulta", auto_now=True, null=False, blank=False)
    reason = models.CharField(
        "Motivo da Consulta", max_length=200, null=False, blank=False
    )
    current_weight = models.FloatField("Peso Atual", null=False, blank=False)
    current_drugs = models.TextField("Medicamento Atual", null=False, blank=True)
    prescribed_drugs = models.TextField(
        "Medicamentos Prescritos", null=False, blank=False
    )
    prescribed_exams = models.TextField("Exames Prescritos", null=False, blank=False)

    class Meta:
        verbose_name = "consulta"
        verbose_name_plural = "consultas"

    def __str__(self):
        return f"{self.pet.name} - {self.date}"
