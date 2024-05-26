import django.db.models

import users.models


class Card(django.db.models.Model):
    card_users = django.db.models.ManyToManyField(
        users.models.User,
        related_name="cards",
    )
    last_numbers = django.db.models.CharField(max_length=20, verbose_name="номер карты")

    class Meta:
        verbose_name = "карта"
        verbose_name_plural = "карты"

    def __str__(self):
        return f"{self.last_numbers}"
