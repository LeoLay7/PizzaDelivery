# Generated by Django 5.0.3 on 2024-05-05 02:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0010_orderedproduct_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="baseproduct",
            name="extra_ingredients",
            field=models.ManyToManyField(
                blank=True,
                related_name="extra",
                to="products.ingredient",
                verbose_name="доп ингредиенты",
            ),
        ),
        migrations.AlterField(
            model_name="baseproduct",
            name="ingredients",
            field=models.ManyToManyField(
                blank=True,
                related_name="ingredients",
                to="products.ingredient",
                verbose_name="ингредиенты",
            ),
        ),
        migrations.AlterField(
            model_name="orderedproduct",
            name="added_ingredient",
            field=models.ManyToManyField(
                blank=True, related_name="added", to="products.ingredient"
            ),
        ),
        migrations.AlterField(
            model_name="orderedproduct",
            name="removed_ingredient",
            field=models.ManyToManyField(
                blank=True, related_name="removed", to="products.ingredient"
            ),
        ),
        migrations.AlterField(
            model_name="orderedproduct",
            name="size",
            field=models.CharField(
                default="medium", max_length=30, null=True, verbose_name="размер"
            ),
        ),
    ]