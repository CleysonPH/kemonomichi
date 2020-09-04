from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(
        "Data de Criação", auto_now=False, auto_now_add=True
    )
    last_modified = models.DateTimeField(
        "Última Atualização", auto_now=True, auto_now_add=False
    )

    class Meta:
        abstract = True
