import django.db.models

import users.models
import products.models
import cart.managers
import django.core.exceptions


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

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзины"

    def __str__(self):
        return f"{self.user.name} cart"

    def change_product_quantity(self, quantity, product=None, return_product=False, removed_ingredients=None,
                                added_ingredients=None, **kwargs):
        if product is None:
            if removed_ingredients is None and added_ingredients is None:
                product = self.products.all().get(**kwargs)
            else:
                same_products = self.products.all().filter(**kwargs)
                for same_product in same_products:
                    if (set(same_product.added_ingredient.all()) == set(added_ingredients) and
                            set(same_product.removed_ingredient.all()) == set(removed_ingredients)):
                        product = same_product
                        break
                if product is None:
                    raise django.core.exceptions.ObjectDoesNotExist

        if isinstance(quantity, str):
            if quantity[0] == "+":
                value = int(quantity[1:])
                quantity = product.quantity + value
            elif quantity[0] == "-":
                value = int(quantity[1:])
                quantity = product.quantity - value
            else:
                raise ValueError("if quantity is str, it should starts with + or -")

        if quantity < product.quantity:
            self.products_sum -= product.amount(full_price=False) * (product.quantity - quantity)
        elif quantity > product.quantity:
            self.products_sum += product.amount(full_price=False) * (quantity - product.quantity)
        else:
            raise ValueError("new product quantity should be different of saved quantity")
        self.save()

        product.quantity = quantity
        product.save()
        if return_product:
            return product

    def add_product(self, product):
        self.products.add(product)
        self.products_sum += product.amount()
        self.save()

    def remove_product(self, product):
        self.products.remove(product)
        self.products_sum -= product.amount()
        self.save()

    def get_products(self):
        return self.products.all().order_by("-base_product__product_type__name", "base_product__name", "size")

    def clear(self):
        self.products.clear()
        self.products_sum = 0
        self.save()
