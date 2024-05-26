import django.forms
import django.core.exceptions

import cart.tools
import products.models


class CartPaymentForm(django.forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["payment_method"] = django.forms.ModelChoiceField(
            queryset=user.cards.all(),
            label="Выберите карту",
            widget=django.forms.Select(attrs={"id": "payment-select"}),
        )
        self.fields["addresses"] = django.forms.ModelChoiceField(
            queryset=user.addresses.all(),
            label="Адрем доставки",
            widget=django.forms.Select(attrs={"id": "address-select"})
        )
        self.fields["time"] = django.forms.ChoiceField(
            choices=cart.tools.order_time,
            label="Ко времени",
            required=False,
        )
        self.fields["comment"] = django.forms.CharField(
            required=False,
            widget=django.forms.Textarea(attrs={"class": "form-control"}),
            label="Комментарий к доставке",
        )


class EditProductForm(django.forms.Form):
    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)

        removed_ingredients = product.removed_ingredient.all()
        added_ingredients = product.added_ingredient.all()
        self.ingredients = {}

        for ingredient in product.base_product.can_delete.all():
            fieldname = "remove_" + str(ingredient.pk)
            data = {
                "label": ingredient.name,
                "required": False,
                "initial": True,
            }
            if ingredient in removed_ingredients:
                data["initial"] = False
            self.fields[fieldname] = django.forms.BooleanField(**data)
            self.ingredients[fieldname] = ingredient

        for ingredient in product.base_product.extra_ingredients.all():
            fieldname = "add_" + str(ingredient.pk)
            data = {
                "label": ingredient.name,
                "required": False,
                "initial": False,
            }
            if ingredient in added_ingredients:
                data["initial"] = True
            self.fields[fieldname] = django.forms.BooleanField(**data)
            self.ingredients[fieldname] = ingredient

        self.fields["quantity"] = django.forms.IntegerField(
            min_value=1,
            max_value=product.quantity,
            label="Количество",
            initial=1,
        )

        self.initial_data = self.get_data()

    def get_data(self):
        data = {}
        for field in self.fields:
            if field.split("_")[0] in ["add", "remove"]:
                data[field] = self.fields[field].initial
        return data

    def get_ingredient_from_field(self, field_name):
        try:
            if "_" in field_name:
                pk = int(field_name.split("_")[1])
                return products.models.Ingredient.objects.get(pk=pk)
        except (ValueError, products.models.Ingredient.DoesNotExist):
            return None

    def clean(self):
        cleaned_data = super().clean()

        removed_ingredients_id = []
        added_ingredients_id = []
        for key in cleaned_data:
            if "_" in key:
                value = cleaned_data.get(key)
                pk = int(key.split("_")[1])
                if key.startswith("add_") and value:
                    added_ingredients_id.append(pk)
                elif key.startswith("remove_") and not value:
                    removed_ingredients_id.append(pk)
        if set(removed_ingredients_id).intersection(set(added_ingredients_id)):
            raise django.core.exceptions.ValidationError(
                "Вы не можете одновременно убрать и добавить ингредиент дополнительно",
                code="invalid",
            )

        new_data = cleaned_data.copy()
        del new_data["quantity"]

        cleaned_data["is_edited"] = True
        if new_data == self.initial_data:
            cleaned_data["is_edited"] = False

        cleaned_data["removed_ingredients_id"] = removed_ingredients_id
        cleaned_data["added_ingredients_id"] = added_ingredients_id
        return cleaned_data
