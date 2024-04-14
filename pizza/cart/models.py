import django.db.models

import users.models
import products.models


class Cart(django.db.models.Model):
    user = django.db.models.OneToOneField(
        users.models.User,
        on_delete=django.db.models.CASCADE,
    )
    products = django.db.models.ManyToManyField(
        products.models.OrderedProduct,
        blank=True,
    )
