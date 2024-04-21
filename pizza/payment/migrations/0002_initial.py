# Generated by Django 5.0.3 on 2024-04-12 10:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("payment", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentmethod",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="paymentmethod",
            name="service",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="payment.paymentservice"
            ),
        ),
    ]
