import django.urls

import products.views


app_name = "products"

urlpatterns = [
    django.urls.path("", products.views.Menu.as_view(), name="menu")
]