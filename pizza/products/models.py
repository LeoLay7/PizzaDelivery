import django.db.models
import products.tools
import products.managers


class Ingredient(django.db.models.Model):
    name = django.db.models.CharField(max_length=50, verbose_name="название")
    image = django.db.models.ImageField(upload_to="ingredients/", null=True, blank=True)
    add_price = django.db.models.PositiveSmallIntegerField(verbose_name="цена добавления в продукт")

    def __str__(self):
        return self.name


class ProductType(django.db.models.Model):
    name = django.db.models.CharField(max_length=30, verbose_name="тип")
    sizable = django.db.models.BooleanField(verbose_name="изменяемый размер")
    sizes = django.db.models.JSONField(verbose_name="размеры")
    extra_fields = django.db.models.JSONField(verbose_name="доп. поля", blank=True, null=True)

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
        related_name="ingredients",
        verbose_name="ингредиенты",
    )
    extra_ingredients = django.db.models.ManyToManyField(
        Ingredient,
        related_name="extra",
        verbose_name="доп ингредиенты",
    )
    editable = django.db.models.BooleanField(verbose_name="редактируемо")
    prices = django.db.models.JSONField(
        verbose_name="цены",
        null=True,
    )

    objects = products.managers.BaseProductManager()

    def __str__(self):
        return self.name


class OrderedProduct(django.db.models.Model):
    base_product = django.db.models.ForeignKey(
        BaseProduct,
        on_delete=django.db.models.CASCADE,
    )
    removed_ingredient = django.db.models.ManyToManyField(
        Ingredient,
        related_name="removed",
        blank=True,
        null=True,
    )
    added_ingredient = django.db.models.ManyToManyField(
        Ingredient,
        related_name="added",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.base_product.name
