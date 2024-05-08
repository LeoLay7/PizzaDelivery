from django.shortcuts import render

import django.views.generic
import products.models


class HomepageView(django.views.generic.TemplateView):
    template_name = "bin/bin.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["base_products"] = products.models.BaseProduct.objects.all()
        return context_data
