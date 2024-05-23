import django.contrib.auth.models
import phonenumber_field.modelfields
import django.core.exceptions
import django.db.models

import users.managers


class Address(django.db.models.Model):
    address = django.db.models.CharField(max_length=300, verbose_name="адрес")
    entrance = django.db.models.CharField(verbose_name="подъезд", max_length=5, null=True)
    floor = django.db.models.CharField(verbose_name="этаж", max_length=5, null=True)
    flat = django.db.models.CharField(verbose_name="квартира", max_length=5, null=True)

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "адреса"

    def __str__(self):
        return self.address


class User(django.contrib.auth.models.AbstractUser):
    name = django.db.models.CharField(max_length=30, verbose_name="имя", blank=True)
    surname = django.db.models.CharField(max_length=30, verbose_name="фамилия", blank=True)
    phone = phonenumber_field.modelfields.PhoneNumberField(
        region="RU",
        verbose_name="телефон",
        blank=True,
    )
    email = django.db.models.EmailField(
        verbose_name="электронная почта",
        unique=True,
    )
    tg_token = django.db.models.CharField(
        max_length=40,
        verbose_name="имя в телеграм",
        blank=True,
    )
    addresses = django.db.models.ManyToManyField(
        Address,
        verbose_name="адресы",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = users.managers.UserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def clean(self):
        super().clean()
        if self.phone:
            if User.objects.filter(phone=self.phone).exclude(pk=self.pk).exists():
                raise django.core.exceptions.ValidationError({"phone": "Этот номер телефона уже используется"})
        if self.tg_token:
            if User.objects.filter(tg_token=self.tg_token).exclude(pk=self.pk).exists():
                raise django.core.exceptions.ValidationError({"tg_token": "Аккаунт с таким логином уже существует"})
        self.username = self.email

    def __str__(self):
        return f"{self.email} {self.name} {self.surname}"
