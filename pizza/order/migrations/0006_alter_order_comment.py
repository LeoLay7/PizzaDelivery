# Generated by Django 5.0.3 on 2024-05-04 22:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0005_rename_payment_method_order_card_order_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="comment",
            field=models.TextField(blank=True, null=True, verbose_name="комментарий"),
        ),
    ]
