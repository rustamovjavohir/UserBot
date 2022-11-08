import datetime

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from staff.models import Request_price, ITRequestPrice, Workers, getMonthList, Total, Salarys


@receiver(post_save, sender=Request_price)
def postSaveRequestPrice(sender, instance, created, *args, **kwargs):
    if not created:
        ITRequestPrice.objects.filter(secondId=instance.id).update(answer=instance.answer)


@receiver(post_save, sender=Workers)
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        months = getMonthList()
        month = months[int(datetime.date.today().month) - 1]
        year = int(datetime.date.today().year)
        if Total.objects.filter(full_name=instance, year=str(year), month=month).exists():
            pass
        else:
            Total.objects.create(full_name=instance, year=str(year), month=month)


@receiver(post_save, sender=Salarys)
def post_save_salary(sender, instance, created, *args, **kwargs):
    if created:
        if Total.objects.filter(full_name=instance.full_name, year=instance.year, month=instance.month).exists():
            pass
        else:
            Total.objects.create(full_name=instance.full_name, year=instance.year, month=instance.month)


@receiver(post_delete, sender=Salarys)
def delete_save_salary(sender, instance, *args, **kwargs):
    Total.objects.filter(full_name=instance.full_name, year=instance.year, month=instance.month).first().delete()
