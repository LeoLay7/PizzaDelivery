from django.contrib import admin

import order.models


admin.site.register(order.models.Order)
admin.site.register(order.models.OrderStatusLog)