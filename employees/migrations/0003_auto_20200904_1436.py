# Generated by Django 3.1.1 on 2020-09-04 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0002_auto_20200903_1857"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="employee",
            options={
                "ordering": ("-date_joined",),
                "verbose_name": "funcionário",
                "verbose_name_plural": "funcionários",
            },
        ),
    ]
