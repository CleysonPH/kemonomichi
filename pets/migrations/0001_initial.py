# Generated by Django 3.1.1 on 2020-09-02 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("clients", "0002_client"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Nome")),
                ("birth_date", models.DateField(verbose_name="Data de Nascimento")),
                (
                    "specie",
                    models.CharField(
                        choices=[("CA", "Cachorro"), ("GA", "Gato"), ("CO", "Coelho")],
                        max_length=2,
                        verbose_name="Espécie",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("PR", "Preto"),
                            ("BR", "Branco"),
                            ("CI", "Cinza"),
                            ("MA", "Marrom"),
                        ],
                        max_length=2,
                        verbose_name="Cor",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clients.client",
                        verbose_name="Dono",
                    ),
                ),
            ],
            options={
                "verbose_name": "pet",
                "verbose_name_plural": "pets",
            },
        ),
    ]
