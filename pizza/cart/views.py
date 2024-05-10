import django.views.generic
import django.http

import cart.models


class CartView(django.views.generic.ListView):
    template_name = "cart/cart.html"
    model = cart.models.Cart
    context_object_name = "cart"

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.kwargs["pk"]:
            return django.http.Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return cart.models.Cart.objects.get_cart(self.kwargs["pk"])