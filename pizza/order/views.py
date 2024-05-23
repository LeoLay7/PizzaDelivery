import django.views
import django.contrib.auth.mixins

import order.models


class OrderView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.DetailView):
    template_name = "orders/order.html"
    model = order.models.Order
    context_object_name = "order"

    def get_object(self, queryset=None):
        return order.models.Order.objects.view_order(self.kwargs["pk"])
