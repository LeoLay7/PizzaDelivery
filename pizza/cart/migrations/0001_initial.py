# Generated by Django 5.0.3 on 2024-04-12 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
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
                (
                    "products",
                    models.ManyToManyField(blank=True, to="products.orderedproduct"),
                ),
            ],
        ),
    ]
