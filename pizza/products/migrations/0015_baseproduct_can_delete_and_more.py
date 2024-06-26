# Generated by Django 5.0.3 on 2024-05-15 00:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0014_rename_number_orderedproduct_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="baseproduct",
            name="can_delete",
            field=models.ManyToManyField(
                blank=True,
                db_comment="Ингредиенты, которые могут быть удалены. Обязатально должны быть включены в поле ingredients",
                related_name="ingredients_delete_product",
                to="products.ingredient",
                verbose_name="Могут быть удалены",
            ),
        ),
        migrations.AlterField(
            model_name="baseproduct",
            name="extra_ingredients",
            field=models.ManyToManyField(
                blank=True,
                related_name="extra_ingredients_products",
                to="products.ingredient",
                verbose_name="доп ингредиенты",
            ),
        ),
        migrations.AlterField(
            model_name="baseproduct",
            name="ingredients",
            field=models.ManyToManyField(
                blank=True,
                related_name="ingredients_products",
                to="products.ingredient",
                verbose_name="ингредиенты",
            ),
        ),
    ]
