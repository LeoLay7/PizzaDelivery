import django.contrib.auth.models
import phonenumber_field.modelfields
import django.db.models


import users.managers


class Address(django.db.models.Model):
    address = django.db.models.CharField(max_length=300, verbose_name="адрес")




class User(django.contrib.auth.models.AbstractUser):
    name = django.db.models.CharField(max_length=30, verbose_name="имя", blank=True)
    surname = django.db.models.CharField(max_length=30, verbose_name="фамилия", blank=True)
    phone = phonenumber_field.modelfields.PhoneNumberField(
        region="RU",
        unique=True,
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
        unique=True,
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

    def __str__(self):
        return f"{self.name} {self.surname}"
