# Generated by Django 5.0.3 on 2024-05-15 00:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0007_alter_order_date_alter_order_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="дата заказа"),
        ),
    ]
