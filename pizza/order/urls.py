import django.urls

import order.views

app_name = "orders"

urlpatterns = [
    django.urls.path("<int:pk>/", order.views.OrderView.as_view(), name="order"),
]