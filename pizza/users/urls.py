import django.urls
import django.contrib.auth

import users.views

app_name = "users"

urlpatterns = [
    django.urls.path("<int:pk>/", users.views.ProfileView.as_view(), name="profile"),
    django.urls.path("reg/", users.views.RegisterView.as_view(), name="register"),
]
