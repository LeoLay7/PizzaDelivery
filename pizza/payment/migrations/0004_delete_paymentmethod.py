# Generated by Django 5.0.3 on 2024-05-03 21:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0003_alter_order_payment_method"),
        ("payment", "0003_remove_paymentmethod_service_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PaymentMethod",
        ),
    ]