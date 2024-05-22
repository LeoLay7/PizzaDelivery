import django.urls

import cart.views

app_name = "cart"

urlpatterns = [
    django.urls.path("<int:pk>", cart.views.CartView.as_view(), name="user_cart"),
    django.urls.path("payment/<int:pk>", cart.views.PaymentView.as_view(), name="payment"),
    django.urls.path("edit/<int:pk>/", cart.views.EditProductView.as_view(), name="edit_product")
]
