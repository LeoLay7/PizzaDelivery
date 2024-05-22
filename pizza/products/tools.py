products_types = [
    ("Пицца", "Пицца"),
    ("Напиток", "Напиток"),
    ("Закуска", "Закуска"),
    ("Соус", "Соус"),
]

products_sizes = [
    ("Маленький", "Маленький"),
    ("Средний", "Средний"),
    ("Большой", "Большой"),
]


def get_with_ordered_product(model, removed_ingredients, added_ingredients, exclude_data=None, **kwargs):
    res = None
    if exclude_data is None:
        same_objects = model.objects.filter(**kwargs)
    else:
        same_objects = model.objects.filter(**kwargs).exclude(**exclude_data)
    if not same_objects:
        return None
    for obj in same_objects:
        if (set(obj.added_ingredient.all()) == set(added_ingredients) and
                set(obj.removed_ingredient.all()) == set(removed_ingredients)):
            res = obj
            break
    return res