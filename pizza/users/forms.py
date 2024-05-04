import django.contrib.auth.forms
import django.forms

import users.models


class RegisterForm(django.contrib.auth.forms.UserCreationForm):
    class Meta:
        model = users.models.User
        fields = ["email", "password1", "password2"]


class ProfileForm(django.forms.ModelForm):
    class Meta:
        model = users.models.User
        fields = ["name", "surname", "phone", "email", "tg_token"]


class AddAddressForm(django.forms.ModelForm):
    class Meta:
        model = users.models.Address
        fields = ["address"]


