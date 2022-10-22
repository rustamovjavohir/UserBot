from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from staff.models import Request_price, ITRequestPrice


@receiver(post_save, sender=Request_price)
def postSaveRequestPrice(sender, instance, created, *args, **kwargs):
    if not created:
        ITRequestPrice.objects.filter(secondId=instance.id).update(answer=instance.answer)

