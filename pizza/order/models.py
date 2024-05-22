import django.db.models
import django.db.models.signals
import django.dispatch

import users.models
import products.models
import payment.models

from order.tools import statuses
import order.managers


class Order(django.db.models.Model):
    user = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="orders",
        verbose_name="пользователь"
    )
    price = django.db.models.IntegerField(
        verbose_name="сумма заказа",
        null=True,
    )
    products = django.db.models.ManyToManyField(
        products.models.OrderedProduct,
        verbose_name="продукты",
    )
    status = django.db.models.CharField(
        choices=statuses,
        max_length=30,
        verbose_name="статус",
        default='Готовится'
    )
    address = django.db.models.ForeignKey(
        users.models.Address,
        on_delete=django.db.models.SET_NULL,
        verbose_name="адрес",
        null=True
    )
    card = django.db.models.ForeignKey(
        payment.models.Card,
        on_delete=django.db.models.SET_NULL,
        verbose_name="способ оплаты",
        null=True
    )
    date = django.db.models.DateTimeField(verbose_name="дата заказа", auto_now_add=True)
    to_time = django.db.models.TimeField(verbose_name="доставка ко времени", blank=True)
    comment = django.db.models.TextField(verbose_name="комментарий", blank=True, null=True,)

    objects = order.managers.OrderManager()

    def __str__(self):
        return f"{self.user.name} {self.price} {self.address}"


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


@django.dispatch.receiver(django.db.models.signals.pre_save, sender=Order)
def create_order_status_log(sender, instance, **kwargs):
    if not instance.pk:
        return

    previous = Order.objects.get(pk=instance.pk)
    if previous.status != instance.status:
        OrderStatusLog.objects.create(
            order=instance,
            from_status=previous.status,
            to_status=instance.status
        )