import django.forms

import payment.models


class AddCardForm(django.forms.ModelForm):
    class Meta:
        model = payment.models.Card
        fields = ["last_numbers"]