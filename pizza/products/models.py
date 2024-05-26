import django.db.models
import products.tools
import products.managers
import django.core.exceptions


class Ingredient(django.db.models.Model):
    name = django.db.models.CharField(max_length=50, verbose_name="название")
    image = django.db.models.ImageField(upload_to="ingredients/", null=True, blank=True)
    add_price = django.db.models.PositiveSmallIntegerField(verbose_name="цена добавления в продукт")

    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиент"

    def __str__(self):
        return self.name


class ProductType(django.db.models.Model):
    name = django.db.models.CharField(max_length=30, verbose_name="тип")
    sizable = django.db.models.BooleanField(verbose_name="изменяемый размер")
    sizes = django.db.models.JSONField(verbose_name="размеры", blank=True, null=True)
    extra_fields = django.db.models.JSONField(verbose_name="доп. поля", blank=True, null=True)
    label = django.db.models.CharField(max_length=30, verbose_name="тип во мн. числе", null=True, )
    label_id = django.db.models.CharField(max_length=30, verbose_name="тип на анг. языке", null=True, )

    class Meta:
        verbose_name = "тип продукта"
        verbose_name_plural = "Типы продуктов"

    def __str__(self):
        return self.name


class BaseProduct(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to="base_products/",
        blank=True, null=True, verbose_name="фото",
    )
    name = django.db.models.CharField(
        max_length=50,
        verbose_name="название",
        null=True,
    )
    product_type = django.db.models.ForeignKey(
        ProductType,
        on_delete=django.db.models.CASCADE,
        verbose_name="тип продукта",
        null=True,
    )
    sizable = django.db.models.BooleanField(verbose_name="изменяемый размер", default=False)
    ingredients = django.db.models.ManyToManyField(
        Ingredient,
        related_name="ingredients_products",
        verbose_name="ингредиенты",
        blank=True,
    )
    extra_ingredients = django.db.models.ManyToManyField(
        Ingredient,
        related_name="extra_ingredients_products",
        verbose_name="доп ингредиенты",
        blank=True,
    )
    can_delete = django.db.models.ManyToManyField(
        Ingredient,
        related_name="ingredients_delete_product",
        verbose_name="Могут быть удалены",
        db_comment="Ингредиенты, которые могут быть удалены. Обязатально должны быть включены в поле ingredients",
        blank=True,
    )
    editable = django.db.models.BooleanField(verbose_name="редактируемо")
    prices = django.db.models.JSONField(
        verbose_name="цены",
        null=True,
    )

    objects = products.managers.BaseProductManager()

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    def __str__(self):
        return self.name

    def get_ingredients(self):
        return ", ".join([str(ingredient) for ingredient in self.ingredients.all()]).capitalize()

    def get_sizes(self):
        return self.product_type.sizes


class OrderedProduct(django.db.models.Model):
    base_product = django.db.models.ForeignKey(
        BaseProduct,
        on_delete=django.db.models.CASCADE,
        related_name="ordered_products"
    )
    removed_ingredient = django.db.models.ManyToManyField(
        Ingredient,
        related_name="removed",
        blank=True,
    )
    added_ingredient = django.db.models.ManyToManyField(
        Ingredient,
        related_name="added",
        blank=True,
    )
    size = django.db.models.CharField(
        max_length=30,
        default="medium",
        verbose_name="размер",
        null=True,
    )
    quantity = django.db.models.IntegerField(
        verbose_name="количество",
        default=1,
    )
    price = django.db.models.IntegerField(
        default=0,
        verbose_name="цена",
    )
    ingredients_price = django.db.models.IntegerField(
        default=0,
        verbose_name="цена добавленных ингредиентов",
    )

    class Meta:
        verbose_name = "заказанный продукт"
        verbose_name_plural = "заказанные продукты"

    def __str__(self):
        return f"{self.base_product.name} {self.quantity} {self.id}"

    def save(self, *args, **kwargs):
        if not self.ingredients_price and self.id and self.added_ingredient:
            self.ingredients_price = sum([ingredient.add_price for ingredient in self.added_ingredient.all()])
        if not self.price:
            self.price = int(self.base_product.prices[self.size]) + self.ingredients_price
        return super().save(*args, **kwargs)

    def amount(self, full_price=True):
        res = self.price + self.ingredients_price
        if full_price:
            return res * self.quantity
        return res

    def get_added_ingredients(self):
        return ", ".join([ingredient.name for ingredient in self.added_ingredient.all()]).capitalize()

    def get_removed_ingredients(self):
        return ", ".join([ingredient.name for ingredient in self.removed_ingredient.all()]).capitalize()

    def edit_ingredients(self, removed_ingredients, added_ingredients, quantity, cart):
        if quantity == self.quantity:
            try:
                same_product = products.tools.get_with_ordered_product(
                    OrderedProduct,
                    removed_ingredients,
                    added_ingredients,
                    exclude_data={"id": self.id},
                    base_product=self.base_product,
                    size=self.size,
                )

                if same_product is not None:
                    cart.change_product_quantity("+" + str(quantity), product=same_product)
                    cart.remove_product(self)
                    self.delete()
                else:
                    raise django.core.exceptions.ObjectDoesNotExist

            except django.core.exceptions.ObjectDoesNotExist:
                self.removed_ingredient.set(removed_ingredients)
                self.added_ingredient.set(added_ingredients)

                new_ingredients_price = sum([ingredient.add_price for ingredient in added_ingredients])

                cart.products_sum += new_ingredients_price - self.ingredients_price
                cart.save()

                self.ingredients_price = new_ingredients_price
                self.save()
        elif quantity < self.quantity:
            try:
                same_product = products.tools.get_with_ordered_product(
                    OrderedProduct,
                    removed_ingredients,
                    added_ingredients,
                    exclude_data={"id": self.id},
                    base_product=self.base_product,
                    size=self.size,
                )
                if same_product is not None:
                    cart.change_product_quantity("+" + str(quantity), product=same_product)
                    cart.change_product_quantity(self.quantity - quantity, product=self)
                else:
                    raise django.core.exceptions.ObjectDoesNotExist
            except django.core.exceptions.ObjectDoesNotExist:
                cart.change_product_quantity(self.quantity - quantity, product=self)
                new_product = OrderedProduct.objects.create(
                    base_product=self.base_product,
                    size=self.size,
                    quantity=quantity
                )
                new_product.removed_ingredient.set(removed_ingredients)
                new_product.added_ingredient.set(added_ingredients)
                new_product.save()

                cart.add_product(new_product)
