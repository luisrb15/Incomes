# Generated by Django 4.2.3 on 2023-10-18 18:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Incomes", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ingreso",
            old_name="ingreso",
            new_name="monto",
        ),
    ]
