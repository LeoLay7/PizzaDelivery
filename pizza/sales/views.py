import django.views.generic


class SalesView(django.views.generic.TemplateView):
    template_name = "sales/sales.html"
