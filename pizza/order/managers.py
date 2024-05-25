import django.db.models


class OrderManager(django.db.models.Manager):
    def view_order(self, pk):
        return self.prefetch_related("products").select_related("user", "address").get(id=pk)