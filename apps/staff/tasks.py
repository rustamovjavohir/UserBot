import json

from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from telegram import Bot

from apps.staff.models import Request_price
from config import settings

bot = Bot(token=settings.S_TOKEN)


@shared_task
def send_message(message):
    bot.send_message(chat_id=settings.ADMIN_ID, text=message)
    return message


@shared_task
def auto_del_request(message_id, chat_id, request_id):
    try:
        Request_price.objects.filter(id=request_id, status=Request_price.Status.PENDING, answer=False).delete()
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as ex:
        text = f"Function: auto_del_request\n" \
               f"order: {request_id}" \
               f"Xatolik yuz berdi: {ex.__str__()}"
        bot.send_message(chat_id=settings.ADMIN_ID, text=text)


inter_schedule, created = IntervalSchedule.objects.get_or_create(
    every=12,
    period=IntervalSchedule.HOURS,
)


def create_task(message):
    periodic_task = PeriodicTask.objects.create(
        interval=inter_schedule,
        name=f'Send message {message}',
        task='apps.tasks.send_message',
        args=(message,),
        one_off=True,
    )
    return periodic_task


def create_auto_delete_req(message_id, chat_id, request_id):
    periodic_task = PeriodicTask.objects.create(
        interval=inter_schedule,
        name=f'Auto delete request {request_id}',
        task='apps.staff.tasks.auto_del_request',
        args=json.dumps([message_id, chat_id, request_id]),
        one_off=True,
    )
    return periodic_task
