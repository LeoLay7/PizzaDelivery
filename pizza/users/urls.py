import django.urls
from django.contrib.auth import views as auth_views

import users.views

app_name = "users"

urlpatterns = [
    django.urls.path("<int:pk>/", users.views.ProfileView.as_view(), name="profile"),
    django.urls.path("register/", users.views.RegisterView.as_view(), name="register"),
]
