# Generated by Django 5.0.3 on 2024-05-03 23:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0004_alter_order_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="payment_method",
            new_name="card",
        ),
        migrations.AddField(
            model_name="order",
            name="price",
            field=models.IntegerField(null=True, verbose_name="сумма заказа"),
        ),
    ]
