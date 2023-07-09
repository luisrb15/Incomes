# Generated by Django 4.2.3 on 2023-07-09 07:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Incomes", "0002_alter_resident_dni"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cuota",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("precio", models.IntegerField(default=0)),
                ("ultima_actualizacion", models.DateField()),
                ("frecuencia_actualizaciones", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Ingreso",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateField(default=datetime.datetime.now)),
                ("ingreso", models.IntegerField(default=0)),
                (
                    "cuota",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Incomes.cuota"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Residente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=50)),
                ("apellido", models.CharField(max_length=50)),
                ("apodo", models.CharField(default="sin apodo", max_length=50)),
                ("dni", models.IntegerField(unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="income",
            name="fee",
        ),
        migrations.RemoveField(
            model_name="income",
            name="resident",
        ),
        migrations.DeleteModel(
            name="Fee",
        ),
        migrations.DeleteModel(
            name="Income",
        ),
        migrations.DeleteModel(
            name="Resident",
        ),
        migrations.AddField(
            model_name="ingreso",
            name="residente",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Incomes.residente"
            ),
        ),
        migrations.AddField(
            model_name="cuota",
            name="residente",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="Incomes.residente"
            ),
        ),
    ]
