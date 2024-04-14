import django.db.models

import users.models
import products.models
import payment.models

from order.tools import statuses


class Order(django.db.models.Model):
    user = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь"
    )
    products = django.db.models.ManyToManyField(
        products.models.OrderedProduct,
        verbose_name="продукты",
    )
    status = django.db.models.CharField(
        choices=statuses,
        max_length=30,
        verbose_name="статус",
    )
    address = django.db.models.ForeignKey(
        users.models.Address,
        on_delete=django.db.models.SET_NULL,
        verbose_name="адрес",
        null=True
    )
    payment_method = django.db.models.ForeignKey(
        payment.models.PaymentMethod,
        on_delete=django.db.models.SET_NULL,
        verbose_name="способ оплаты",
        null=True
    )
    date = django.db.models.DateField(verbose_name="дата заказа")
    to_time = django.db.models.TimeField(verbose_name="доставка ко времени")
    comment = django.db.models.TextField(verbose_name="комментарий")


class OrderStatusLog(django.db.models.Model):
    order = django.db.models.ForeignKey(
        Order,
        on_delete=django.db.models.CASCADE,
    )
    from_status = django.db.models.CharField(
        choices=statuses,
        max_length=30,
    )
    to_status = django.db.models.CharField(
        choices=statuses,
        max_length=30,
    )
    time = django.db.models.DateTimeField(
        auto_now_add=True,
    )