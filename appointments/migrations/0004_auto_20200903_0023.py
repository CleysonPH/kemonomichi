# Generated by Django 3.1.1 on 2020-09-03 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0003_auto_20200903_0022"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="prescribed_drugs",
            field=models.TextField(blank=True, verbose_name="Medicamentos Prescritos"),
        ),
    ]
