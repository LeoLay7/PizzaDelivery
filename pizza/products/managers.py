import django.db.models


class BaseProductManager(django.db.models.Manager):
    def get_menu(self):
        return (self.select_related("product_type")
                .order_by("-product_type__name")
                .only("name", "product_type__name", "prices", "image"))

