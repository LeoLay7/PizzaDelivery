import django.views.generic
import django.shortcuts
import django.http
import django.core.exceptions

import users.forms
import payment.forms
import users.models
import payment.models
import products.models


class ProfileAddressView(django.views.View):
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "delete":
            return self.delete(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = users.forms.AddAddressForm()
            return django.shortcuts.render(
                request,
                "includes/add_address_form.html",
                {"form": form},
            )
        else:
            return django.http.JsonResponse({'error': 'Invalid request'})

    def post(self, request, pk, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = users.forms.AddAddressForm(request.POST)
            if form.is_valid():
                try:
                    address = users.models.Address.objects.get(
                        address=form.cleaned_data.get("address"),
                    )
                except django.core.exceptions.ObjectDoesNotExist:
                    address = form.save(commit=False)
                    address.save()
                user = django.shortcuts.get_object_or_404(users.models.User, pk=pk)
                if address not in user.addresses.all():
                    user.addresses.add(address)
                    user.save()
                else:
                    return django.http.JsonResponse({"error": "Этот адрес уже добавлен"})

                address_card_html = django.shortcuts.render(
                    request,
                    "includes/profile_address_card.html",
                    {"address": address}
                ).content.decode('utf-8')

                return django.http.JsonResponse(
                    {
                        'success': 'Адрес успешно добавлен',
                        'address_card_html': address_card_html,
                    }
                )
            else:
                return django.http.JsonResponse({'error': form.errors})
        else:
            return django.http.JsonResponse({'error': 'Invalid request'})

    def delete(self, request, user_pk, address_pk, *args, **kwargs):
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                address = users.models.Address.objects.get(pk=address_pk)
                user = users.models.User.objects.get(pk=user_pk)
                user.addresses.remove(address)
                return django.http.JsonResponse({"success": "Адрес успешно удален"})
            else:
                return django.http.JsonResponse({'error': 'Invalid request'})
        except django.core.exceptions.ObjectDoesNotExist:
            return django.http.JsonResponse({"error": "Произошла какая-то ошибка"})


class ProfileCardView(django.views.View):
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "delete":
            return self.delete(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = payment.forms.AddCardForm()
            return django.shortcuts.render(
                request,
                "includes/add_card_form.html",
                {"form": form},
            )
        else:
            return django.http.JsonResponse({'error': 'Invalid request'})

    def post(self, request, pk, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = payment.forms.AddCardForm(request.POST)
            if form.is_valid():
                form.cleaned_data["last_numbers"] = "*" + form.cleaned_data["last_numbers"].strip()[-4:]
                user = django.shortcuts.get_object_or_404(users.models.User, pk=pk)
                try:
                    card = payment.models.Card.objects.get(
                        last_numbers=form.cleaned_data.get("last_numbers")
                    )
                    if user not in card.card_users.all():
                        card.card_users.add(user)
                        card.save()
                    else:
                        return django.http.JsonResponse({"error": "Эта карта уже добавлена"})
                except django.core.exceptions.ObjectDoesNotExist:
                    card = form.save(commit=False)
                    card.last_numbers = "*" + card.last_numbers.strip()[-4:]
                    card.save()
                    card.card_users.set([user])
                    card.save()

                card_card_html = django.shortcuts.render(
                    request,
                    "includes/profile_card_card.html",
                    {"card": card}
                ).content.decode('utf-8')

                return django.http.JsonResponse(
                    {
                        'success': 'Карта успешно добавлена',
                        'card_card_html': card_card_html,
                    }
                )
            else:
                return django.http.JsonResponse({'error': form.errors})
        else:
            return django.http.JsonResponse({'error': 'Invalid request'})

    def delete(self, request, user_pk, card_pk, *args, **kwargs):
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                card = payment.models.Card.objects.get(pk=card_pk)
                user = users.models.User.objects.get(pk=user_pk)
                card.card_users.remove(user)
                if not card.card_users.all():
                    card.delete()
                return django.http.JsonResponse({"success": "Карта успешно удалена"})
            else:
                return django.http.JsonResponse({'error': 'Invalid request'})
        except django.core.exceptions.ObjectDoesNotExist:
            return django.http.JsonResponse({"error": "Произошла какая-то ошибка"})


class MenuView(django.views.View):
    def post(self, request, pk, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if request.user.is_authenticated:
                user = request.user
                cart = user.cart
                try:
                    cart.change_product_quantity("+1", base_product__id=pk, size="medium")
                except django.core.exceptions.ObjectDoesNotExist:
                    base_product = products.models.BaseProduct.objects.get(pk=pk)
                    ordered_product = products.models.OrderedProduct.objects.create(
                        base_product=base_product,
                    )
                    cart.add_product(ordered_product)
                return django.http.JsonResponse({"success": "Товар успешно добавлен в корзину"})
            else:
                return django.http.JsonResponse({"error": "Чтобы добавить товар в корзину, сначала зарегистрируйтесь"})

        else:
            return django.http.JsonResponse({'error': 'Invalid request'})


class CartView(django.views.View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        if data.get("action") == "update_quantity":
            cart = request.user.cart
            product = cart.change_product_quantity(
                int(data.get("quantity")),
                return_product=True,
                id=data.get("product_id")
            )
            return django.http.JsonResponse(
                {
                    "success": "Количество изменено",
                    "amount": cart.products_sum,
                    "product_amount": product.amount(),
                }
            )

        elif data.get("action") == "update_size":
            cart = request.user.cart
            product = cart.products.all().get(id=int(data.get("product_id")))
            new_size = data.get("size")
            old_product_card = {"card_id": product.id, "action": "edit", "html": ""}
            new_product_card = {"card_id": 0, "action": "edit", "html": ""}

            try:
                new_product = cart.change_product_quantity(
                    "+1",
                    return_product=True,
                    base_product=product.base_product,
                    size=new_size,
                    added_ingredients=product.added_ingredient.all(),
                    removed_ingredients=product.removed_ingredient.all(),
                )

                new_product_card["card_id"] = new_product.id
                new_product_card["action"] = "edit"
                new_product_card["html"] = django.shortcuts.render(
                        request,
                        "includes/cart_product_card.html",
                        {"product": new_product}
                    ).content.decode('utf-8')
            except django.core.exceptions.ObjectDoesNotExist:
                new_product = products.models.OrderedProduct.objects.create(
                    base_product=product.base_product,
                    size=new_size,
                )
                new_product.added_ingredient.set(product.added_ingredient.all())
                new_product.removed_ingredient.set(product.removed_ingredient.all())
                new_product.save()
                cart.add_product(new_product)

                new_product_card["card_id"] = new_product.id
                new_product_card["action"] = "add"
                new_product_card["html"] = django.shortcuts.render(
                    request,
                    "includes/cart_product_card.html",
                    {"product": new_product}
                ).content.decode('utf-8')

            if product.quantity == 1:
                cart.remove_product(product)
                product.delete()

                old_product_card["action"] = "delete"
            else:
                cart.change_product_quantity("-1", product=product)

                old_product_card["action"] = "edit"
                old_product_card["html"] = django.shortcuts.render(
                        request,
                        "includes/cart_product_card.html",
                        {"product": product}
                    ).content.decode('utf-8')
            return django.http.JsonResponse(
                {
                    "success": "Размер изменен успешно",
                    "old_card": old_product_card,
                    "new_card": new_product_card,
                    "amount": cart.products_sum,
                }, )
        elif data.get("action") == "delete product":
            cart = request.user.cart
            product = products.models.OrderedProduct.objects.get(id=data.get("product_id"))
            cart.remove_product(product)
            if not product.carts.all():
                product.delete()
            return django.http.JsonResponse({"success": "Продукт успешно удален", "amount": cart.products_sum})
        else:
            return django.http.JsonResponse({"error": "Invalid request"})
