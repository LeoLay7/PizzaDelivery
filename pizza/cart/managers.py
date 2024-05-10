import django.db.models


class CartManager(django.db.models.Manager):
    def get_cart(self, user_id):
        return self.prefetch_related("products").get(user=user_id)
