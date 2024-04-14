from django.contrib import admin

import products.models

admin.site.register(products.models.OrderedProduct)
admin.site.register(products.models.BaseProduct)
admin.site.register(products.models.Ingredient)