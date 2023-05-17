import threading

import requests
from telegram import Update

from config.settings import URL_1C, LOGIN_1C, PASSWORD_1C
from apps.staff.buttons import foodMenuButton
from apps.staff.models import Request_price, ITRequestPrice, Data
from apps.staff.utils import getWorker, notificationBot
from apps.staff.views import isWorker


def inline(update: Update, context):
    user_id = update.callback_query.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    data = update.callback_query.data.split("_")
    if isWorker(user_id):
        if len(data) == 2 and data[0] == 'done':
            update.callback_query.message.edit_reply_markup()
            req = Request_price.objects.get(pk=data[1])
            if req.is_deleted:
                department = "00-000022"
            else:
                department = req.department_id
            url = f"{URL_1C}hs/radius_bot/create_applications"
            auth = (LOGIN_1C, PASSWORD_1C)
            js = {
                "id": str(req.pk),
                "department": department,
                "price": req.price,
                "avans": True,
                "comment": req.month
            }
            res = requests.post(url=url, auth=auth, json=js)
            if 'success' in list(res.json().keys()):
                update.callback_query.message.reply_text("✅So`rov kassaga yuborildi")
                text = f"✅So`rov tasdiqlandi, kassaga chiqishingiz mumkin ID: {req.pk}"
                if req.is_deleted:
                    req = ITRequestPrice.objects.get(secondId=data[1])
                    for i in req.workers.all():
                        context.bot.send_message(chat_id=i.telegram_id, text=text)
                else:
                    for i in req.workers.all():
                        context.bot.send_message(chat_id=i.full_name.telegram_id, text=text)
            else:
                update.callback_query.message.reply_text("🚫Xatolik yuz berdi")
        elif len(data) == 2 and data[0] == 'not':
            update.callback_query.message.edit_reply_markup()
            req = Request_price.objects.filter(pk=data[1]).first()
            if req:
                try:
                    if req.is_deleted:
                        req = ITRequestPrice.objects.get(secondId=data[1])
                        for i in req.workers.all():
                            context.bot.send_message(chat_id=i.telegram_id,
                                                     text=f"❌So`rov bo`lim boshlig`i tomonidan rad etildi,"
                                                          f" ID: {req.secondId}")
                    for i in req.workers.all():
                        context.bot.send_message(chat_id=i.full_name.telegram_id,
                                                 text=f"❌So`rov {getWorker(user_id).full_name} "
                                                      f"tomonidan rad etildi, ID: {req.pk}")
                    Request_price.objects.get(pk=data[1]).delete()
                    update.callback_query.message.reply_text("❌So`rov rad etildi")
                except Exception as ex:
                    print(ex)
        elif len(data) == 2 and data[1] == "seat":
            step.update({"step": 0})
            update.callback_query.delete_message()
            context.bot.send_message(chat_id=user_id, text="Habar jonatildi", reply_markup=foodMenuButton())
            message = f"Oshxonada <strong>{data[0]}</strong> ta joy bor"
            notification_bot_thread = threading.Thread(target=notificationBot, args=(message,))
            notification_bot_thread.start()
            Data.objects.filter(telegram_id=user_id).update(data=step)
