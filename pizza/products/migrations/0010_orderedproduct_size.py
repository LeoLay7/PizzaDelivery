# Generated by Django 5.0.3 on 2024-05-04 22:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0009_producttype_label_producttype_label_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderedproduct",
            name="size",
            field=models.CharField(max_length=30, null=True, verbose_name="размер"),
        ),
    ]
