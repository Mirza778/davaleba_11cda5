from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product: {self.name} (id={self.pk})"

class AuditLog(models.Model):
    model_name = models.CharField(max_length=100)
    object_pk = models.IntegerField()
    deleted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[AuditLog] {self.model_name} #{self.object_pk} — {self.deleted_at:%Y-%m-%d %H:%M:%S}"

    class Meta:
        ordering = ['-deleted_at']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped',   'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),]

    customer_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} — {self.customer_name} [{self.status}]"

    def save(self, *args, **kwargs):
        from .signals import order_status_changed

        old_status = None
        if self.pk:
            try:
                old_status = Order.objects.get(pk=self.pk).status
            except Order.DoesNotExist:
                pass

        super().save(*args, **kwargs)
        if old_status is not None and old_status != self.status:
            order_status_changed.send(sender=self.__class__,
                instance=self,old_status=old_status,new_status=self.status, )
