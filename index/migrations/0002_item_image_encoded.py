# Generated by Django 4.1.13 on 2024-04-21 06:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("index", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="image_encoded",
            field=models.TextField(blank=True),
        ),
    ]
