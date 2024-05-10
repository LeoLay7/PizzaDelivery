import django.db.models

import users.models
import products.models
import cart.managers


class Cart(django.db.models.Model):
    user = django.db.models.OneToOneField(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="cart",
    )
    products = django.db.models.ManyToManyField(
        products.models.OrderedProduct,
        blank=True,
        related_name="carts",
    )
    products_sum = django.db.models.IntegerField(
        default=0,
        verbose_name="сумма заказа",
    )

    objects = cart.managers.CartManager()

    def change_product_quantity(self, quantity, product=None, return_product=False, **kwargs):
        if product is None:
            product = self.products.all().get(**kwargs)

        if isinstance(quantity, str):
            if quantity[0] == "+":
                quantity = product.quantity + 1
            elif quantity[0] == "-":
                quantity = product.quantity - 1
            else:
                raise ValueError("if quantity is str, it should start with + or -")

        if quantity < product.quantity:
            self.products_sum -= product.price
        elif quantity > product.quantity:
            self.products_sum += product.price
        else:
            raise ValueError("new product quantity should be different of saved quantity")
        self.save()

        product.quantity = quantity
        product.save()
        if return_product:
            return product

    def add_product(self, product):
        self.products.add(product)
        self.products_sum += product.price
        self.save()

    def remove_product(self, product):
        self.products.remove(product)
        self.products_sum -= product.price * product.quantity
        self.save()