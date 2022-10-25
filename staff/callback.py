import requests
from telegram import Update

from config.settings import URL_1C, LOGIN_1C, PASSWORD_1C
from staff.models import Request_price, ITRequestPrice
from staff.views import isWorker


def inline(update: Update, context):
    user_id = update.callback_query.from_user.id
    data = update.callback_query.data.split("_")
    if isWorker(user_id):
        if len(data) == 2 and data[0] == 'done':
            update.callback_query.message.edit_reply_markup()
            req = Request_price.objects.get(pk=data[1])
            if req.is_deleted:
                department = "00-000022"
            else:
                department = req.department_id
            url = f"{URL_1C}ut3/hs/create_applications"
            auth = (LOGIN_1C, PASSWORD_1C)
            js = {
                "id": str(req.pk),
                "department": department,
                "price": req.price,
                "avans": True,
                "comment": ""
            }
            res = requests.post(url=url, auth=auth, json=js)
            print(res.json())
            if 'success' in list(res.json().keys()):
                update.callback_query.message.reply_text("✅So`rov kassaga yuborildi")
                text = f"✅So`rov tasdiqlandi, kassaga chiqishingiz mumkin ID: {req.pk}"
                if req.is_deleted:
                    req = ITRequestPrice.objects.get(secondId=data[1])
                    for i in req.workers.all():
                        print(i.telegram_id)
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
                                                 text=f"❌So`rov bo`lim boshlig`i tomonidan rad etildi, ID: {req.pk}")
                    Request_price.objects.get(pk=data[1]).delete()
                    update.callback_query.message.reply_text("❌So`rov rad etildi")
                except Exception as ex:
                    print(ex)
