import django.views.generic
import django.http
import django.shortcuts
import django.core.exceptions
import django.contrib.auth.mixins

import cart.models
import cart.forms
import products.models
import users.models
import order.models


class CartView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.ListView):
    template_name = "cart/cart.html"
    model = cart.models.Cart
    context_object_name = "cart"

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.kwargs["pk"]:
            return django.http.Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return cart.models.Cart.objects.get_cart(self.kwargs["pk"])


class PaymentView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.FormView):
    form_class = cart.forms.CartPaymentForm
    template_name = "cart/payment.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = users.models.User.objects.get(id=int(self.kwargs["pk"]))
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["amount"] = cart.models.Cart.objects.get(user__id=self.kwargs["pk"]).products_sum
        return data

    def form_valid(self, form):
        data = form.cleaned_data
        payment = data.get("payment_method")
        address = data.get("addresses")
        to_time = data.get("time")
        comment = data.get("comment")

        user = users.models.User.objects.get(id=int(self.kwargs["pk"]))
        cart = user.cart
        data = {
            'user': user,
            'price': cart.products_sum,
            'address': address,
            'card': payment,
            'comment': comment,
        }
        if to_time != 'fast':
            data["to_time"] = to_time

        new_order = order.models.Order.objects.create(**data)
        new_order.products.set(cart.products.all())
        new_order.save()

        user.cart.clear()

        return django.shortcuts.redirect("products:menu")


class EditProductView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.UpdateView):
    model = products.models.OrderedProduct
    form_class = cart.forms.EditProductForm
    template_name = "cart/edit_product.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs["pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj = self.get_object()
        kwargs["product"] = obj
        del kwargs["instance"]

        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        if data.get("is_edited"):
            product = self.get_object()
            user_cart = self.request.user.cart

            product.edit_ingredients(
                products.models.Ingredient.objects.filter(id__in=data.get("removed_ingredients_id")),
                products.models.Ingredient.objects.filter(id__in=data.get("added_ingredients_id")),
                int(data["quantity"]),
                user_cart,
            )

        return django.shortcuts.redirect("cart:user_cart", pk=self.request.user.id)
