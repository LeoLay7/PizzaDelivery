# Generated by Django 5.0.3 on 2024-05-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0015_baseproduct_can_delete_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderedproduct",
            name="ingredients_price",
            field=models.IntegerField(
                default=0, verbose_name="цена добавленных ингредиентов"
            ),
        ),
    ]
