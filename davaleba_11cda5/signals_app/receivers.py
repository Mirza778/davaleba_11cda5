from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import AuditLog, Order, Product, UserProfile
from .signals import order_status_changed

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(pre_delete, sender=Product)
def log_product_deletion(sender, instance, **kwargs):
    AuditLog.objects.create(
        model_name=sender.__name__,object_pk=instance.pk,)

@receiver(order_status_changed, sender=Order)
def handle_order_status_changed(sender, instance, old_status, new_status, **kwargs):
    print(f"Order #{instance.pk} moved from {old_status} → {new_status}")
