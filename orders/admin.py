from django.contrib import admin
from orders import models


admin.site.register(models.Order)
admin.site.register(models.Payment)
admin.site.register(models.OrderProduct)

# Register your models here.
