import datetime

from django.db import transaction
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

from staff.models import *


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


@transaction.atomic
@receiver(pre_save, sender=Bonus)
def pre_save_bonus(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(id=instance.id).first()
    if old_instance:
        total = Total.objects.filter(full_name=old_instance.full_name, year=old_instance.year,
                                     month=old_instance.month).order_by('-id').first()
        if total:
            if instance.is_deleted:
                total.bonuss_2 -= instance.bonus
                total.paid_2 -= instance.paid
            else:
                total.bonuss_2 += (instance.bonus - old_instance.bonus)
                total.paid_2 += (instance.paid - old_instance.paid)
            total.save()
    else:
        total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                     month=instance.month).order_by('-id').first()
        total.bonuss_2 += instance.bonus
        total.paid_2 += instance.paid
        total.save()


@transaction.atomic
@receiver(pre_delete, sender=Bonus)
def pre_delete_bonus(sender, instance, using, **kwargs):
    total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                 month=instance.month).order_by('-id').first()
    if total:
        total.bonuss_2 -= instance.bonus
        total.paid_2 -= instance.paid
        total.save()


@transaction.atomic
@receiver(pre_save, sender=Leave)
def pre_save_Leave(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(id=instance.id).first()
    if old_instance:
        total = Total.objects.filter(full_name=old_instance.full_name, year=old_instance.year,
                                     month=old_instance.month).order_by('-id').first()
        if total:
            total.vplacheno_2 += (instance.fine - old_instance.fine)
            total.save()
    else:
        total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                     month=instance.month).order_by('-id').first()
        total.vplacheno_2 += instance.fine
        total.save()


@transaction.atomic
@receiver(pre_delete, sender=Leave)
def pre_delete_leave(sender, instance, using, **kwargs):
    total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                 month=instance.month).order_by('-id').first()
    if total:
        total.vplacheno_2 -= instance.fine
        total.save()
