from django.contrib import admin
from .models import UserProfile, Product, AuditLog, Order

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(AuditLog)
admin.site.register(Order)
