import django.urls

import sales.views

app_name = "sales"

urlpatterns = [
    django.urls.path("", sales.views.SalesView.as_view(), name="sales")
]