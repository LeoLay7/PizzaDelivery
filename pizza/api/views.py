import django.views.generic
import django.shortcuts
import django.http
import django.core.exceptions

import users.forms
import payment.forms
import users.models
import payment.models


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