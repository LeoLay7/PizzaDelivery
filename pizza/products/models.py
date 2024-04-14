import django.db.models


class Ingredient(django.db.models.Model):
    name = django.db.models.CharField(max_length=50, verbose_name="название")
    photo = django.db.models.ImageField()
    add_price = django.db.models.PositiveSmallIntegerField(verbose_name="цена добавления в продукт")


class BaseProduct(django.db.models.Model):
    ingredients = django.db.models.ManyToManyField(
        Ingredient,
        related_name="ingredients",
    )
    extra_ingredients = django.db.models.ManyToManyField(
        Ingredient,
        related_name="extra",
    )
    calories = django.db.models.PositiveSmallIntegerField(verbose_name="калории")
    weight = django.db.models.PositiveSmallIntegerField(verbose_name="вес")
    editable = django.db.models.BooleanField(verbose_name="редактируемо")


class OrderedProduct(django.db.models.Model):
    base_product = django.db.models.ForeignKey(
        BaseProduct,
        on_delete=django.db.models.CASCADE,
    )
    removed_ingredient = django.db.models.ManyToManyField(
        Ingredient,
        related_name="removed",
    )
    added_ingredient = django.db.models.ManyToManyField(
        Ingredient,
        related_name="added",
    )