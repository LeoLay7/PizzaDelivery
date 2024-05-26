import django.db.models

import products.models


class BaseProductManager(django.db.models.Manager):
    def get_menu(self):
        return (self.select_related("product_type")
                .order_by("-product_type__name")
                .only("name", "product_type__name", "prices", "image"))

    def get_user_products(self, user, products_num=3):
        orders = user.orders.all()
        if orders:
            ordered_products = products.models.OrderedProduct.objects.filter(order__in=orders)

            base_products_count = ordered_products.values('base_product').annotate(total_quantity=django.db.models.Count('id')).order_by(
                '-total_quantity')

            top_base_product_ids = [item['base_product'] for item in base_products_count[:products_num]]
            top_base_products = products.models.BaseProduct.objects.filter(id__in=top_base_product_ids)

            return top_base_products
        return 0


