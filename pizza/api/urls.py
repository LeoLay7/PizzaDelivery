import django.urls

import api.views

app_name = "api"

urlpatterns = [

]

profile_address = [
    django.urls.path("add_address_form/", api.views.ProfileAddressView.as_view(), name="add_address_form"),
    django.urls.path("add_address/<int:pk>", api.views.ProfileAddressView.as_view(), name="add_address"),
    django.urls.path(
        "delete_address/<int:user_pk>/<int:address_pk>",
        api.views.ProfileAddressView.as_view(),
        name="delete_address",
    ),
]

profile_cards = [
    django.urls.path("add_card_form/", api.views.ProfileCardView.as_view(), name="add_card_form"),
    django.urls.path("add_card/<int:pk>", api.views.ProfileCardView.as_view(), name="add_card"),
    django.urls.path("delete_card/<int:card_pk>/<int:user_pk>", api.views.ProfileCardView.as_view(), name="delete_card")
]

urlpatterns += profile_address
urlpatterns += profile_cards
