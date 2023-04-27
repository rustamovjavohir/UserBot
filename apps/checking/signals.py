from apps.checking.models import Timekeeping
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
from pytz import timezone


@receiver(post_save, sender=Timekeeping)
def pre_save_timekeeping(sender, created, instance, *args, **kwargs):
    if created:
        tz = timezone('Asia/Tashkent')
        instance.date = datetime.now(tz=tz).date()
