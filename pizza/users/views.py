import django.views.generic
import django.shortcuts
import django.views.generic.edit
import django.urls
import django.contrib.auth.mixins

import users.forms
import users.models


class RegisterView(django.views.generic.FormView):
    template_name = "registration/register.html"
    form_class = users.forms.RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        users.models.User.objects.create_user(data["email"], data["password1"])
        return django.shortcuts.redirect("login")

    def get_success_url(self):
        return django.shortcuts.reverse("login")


class ProfileView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.UpdateView):
    template_name = "users/profile.html"
    form_class = users.forms.ProfileForm
    model = users.models.User

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        info = users.models.User.objects.user_profile_info(self.kwargs["pk"], profile_form=False)
        data["user"] = info

        return data

    def get_success_url(self):
        return django.shortcuts.reverse("users:profile", args=[self.kwargs["pk"]])

    def get_object(self, queryset=None):
        return users.models.User.objects.user_profile_info(self.kwargs["pk"], profile_form=True)