# Generated by Django 5.0 on 2024-01-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "slug",
                    models.SlugField(blank=True, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
    ]
