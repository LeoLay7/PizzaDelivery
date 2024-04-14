import django.db.models


import users.models


class PaymentService(django.db.models.Model):
    name = django.db.models.CharField(max_length=30, verbose_name="название")
    template_info = django.db.models.JSONField(verbose_name="шаблон информации")


class PaymentMethod(django.db.models.Model):
    user = django.db.models.ForeignKey(users.models.User, on_delete=django.db.models.CASCADE)
    service = django.db.models.ForeignKey(
        PaymentService,
        on_delete=django.db.models.CASCADE,
    )
    info = django.db.models.JSONField(verbose_name="информация")
