import django.views.generic

import products.models


class Menu(django.views.generic.ListView):
    template_name = "menu/catalog.html"
    model = products.models.BaseProduct
    context_object_name = "products"

    def get_queryset(self):
        return products.models.BaseProduct.objects.get_menu()

