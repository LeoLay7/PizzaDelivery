from django.shortcuts import render

import django.views.generic
import products.models


class HomepageView(django.views.generic.TemplateView):
    template_name = "homepage/home.html"
