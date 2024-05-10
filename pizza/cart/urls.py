import django.urls

import cart.views

app_name = "cart"

urlpatterns = [
    django.urls.path("<int:pk>", cart.views.CartView.as_view(), name="user_cart")
]
