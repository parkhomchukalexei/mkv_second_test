from django.db.models.signals import post_save
from django.dispatch import receiver

from order_controller.models import Order
from .tasks import send_order_email


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if created:
        send_order_email.delay(instance.pk)