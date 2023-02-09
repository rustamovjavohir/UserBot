import datetime

from django.db import transaction
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from telegram import Bot

from config.settings import TELEGRAM_TOKEN
from staff.models import *

bot = Bot(TELEGRAM_TOKEN)


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


#  bug ----------
@receiver(post_save, sender=Salarys)
def post_save_salary(sender, instance, created, *args, **kwargs):
    if created:
        if Total.objects.filter(full_name=instance.full_name, year=instance.year, month=instance.month).exists():
            pass
        else:
            Total.objects.create(full_name=instance.full_name, year=instance.year, month=instance.month,
                                 oklad_1=instance.salary)
    else:
        Total.objects.filter(full_name=instance.full_name, year=instance.year,
                             month=instance.month).update(oklad_1=instance.salary)


@receiver(post_delete, sender=Salarys)
def delete_save_salary(sender, instance, *args, **kwargs):
    total = Total.objects.filter(full_name=instance.full_name, year=instance.year, month=instance.month).first()
    if total:
        text = f"Salarys deleted {total.full_name} {total.month}"
        bot.send_message(chat_id=779890968, text=text)
        total.delete()


@transaction.atomic
@receiver(pre_save, sender=Bonus)
def pre_save_bonus(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(id=instance.id).first()
    if old_instance:
        total = Total.objects.filter(full_name=old_instance.full_name, year=old_instance.year,
                                     month=old_instance.month).order_by('-id').first()
        if total:
            if instance.is_deleted:
                total.bonuss_1 -= instance.bonus
                total.paid_1 -= instance.paid
            else:
                total.bonuss_1 += (instance.bonus - old_instance.bonus)
                total.paid_1 += (instance.paid - old_instance.paid)
            total.save()
    else:
        total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                     month=instance.month).order_by('-id').first()
        if total:
            total.bonuss_1 += instance.bonus
            total.paid_1 += instance.paid
            total.save()


@transaction.atomic
@receiver(pre_delete, sender=Bonus)
def pre_delete_bonus(sender, instance, using, **kwargs):
    total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                 month=instance.month).order_by('-id').first()
    if total:
        total.bonuss_1 -= instance.bonus
        total.paid_1 -= instance.paid
        total.save()


@transaction.atomic
@receiver(pre_save, sender=Leave)
def pre_save_Leave(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(id=instance.id).first()
    if old_instance:
        total = Total.objects.filter(full_name=old_instance.full_name, year=old_instance.year,
                                     month=old_instance.month).order_by('-id').first()
        if total:
            total.vplacheno_1 += (instance.fine - old_instance.fine)
            total.save()
    else:
        total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                     month=instance.month).order_by('-id').first()
        if total:
            total.vplacheno_1 += instance.fine
            total.save()


@transaction.atomic
@receiver(pre_delete, sender=Leave)
def pre_delete_leave(sender, instance, using, **kwargs):
    total = Total.objects.filter(full_name=instance.full_name, year=instance.year,
                                 month=instance.month).order_by('-id').first()
    if total:
        total.vplacheno_1 -= instance.fine
        total.save()


@transaction.atomic
@receiver(pre_delete, sender=Total)
def pre_delete_leave(sender, instance, using, **kwargs):
    text = f"Total deleted {instance.full_name} {instance.month}"
    bot.send_message(chat_id=779890968, text=text)


@transaction.atomic
@receiver(pre_delete, sender=Workers)
def pre_delete_leave(sender, instance, using, **kwargs):
    text = f"Workers deleted {instance.full_name} {instance.department}"
    bot.send_message(chat_id=779890968, text=text)
