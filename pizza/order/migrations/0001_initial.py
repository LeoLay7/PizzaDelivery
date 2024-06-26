# Generated by Django 5.0.3 on 2024-04-12 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("Готовится", "Готовится"),
                            ("Приготовлен", "Приготовлен"),
                            ("Передан курьеру", "Передан курьеру"),
                            ("Доставлен", "Доставлен"),
                        ],
                        max_length=30,
                        verbose_name="статус",
                    ),
                ),
                ("date", models.DateField(verbose_name="дата заказа")),
                ("to_time", models.TimeField(verbose_name="доставка ко времени")),
                ("comment", models.TextField(verbose_name="комментарий")),
            ],
        ),
        migrations.CreateModel(
            name="OrderStatusLog",
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
                    "from_status",
                    models.CharField(
                        choices=[
                            ("Готовится", "Готовится"),
                            ("Приготовлен", "Приготовлен"),
                            ("Передан курьеру", "Передан курьеру"),
                            ("Доставлен", "Доставлен"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "to_status",
                    models.CharField(
                        choices=[
                            ("Готовится", "Готовится"),
                            ("Приготовлен", "Приготовлен"),
                            ("Передан курьеру", "Передан курьеру"),
                            ("Доставлен", "Доставлен"),
                        ],
                        max_length=30,
                    ),
                ),
                ("time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
