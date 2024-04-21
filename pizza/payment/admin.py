from django.contrib import admin

import payment.models


admin.site.register(payment.models.PaymentMethod)
admin.site.register(payment.models.PaymentService)
