import django.views.generic

import products.models
import django.contrib.auth.mixins


class Menu(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.ListView):
    template_name = "menu/menu.html"
    model = products.models.BaseProduct
    context_object_name = "products"

    def get_queryset(self):
        return products.models.BaseProduct.objects.get_menu()

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data["recommended_products"] = products.models.BaseProduct.objects.get_user_products(self.request.user)
        return data

