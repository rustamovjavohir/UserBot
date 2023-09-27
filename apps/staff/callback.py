import threading

import requests
from telegram import Update

from apps.rooms.models import Rooms
from config.settings import URL_1C, LOGIN_1C, PASSWORD_1C
from apps.staff.buttons import foodMenuButton, acceptInlineButton, roomMenuButton, roomListInlineButton, \
    freeRoomHoursInlineButton, avansButton
from apps.staff.models import Request_price, ITRequestPrice, Data
from apps.staff.utils import getWorker, notificationBot, getAvansText, roomTableText, selectBookTime, freeRoomHours, \
    freeRoomEndHours, send_message_to_group
from apps.staff.views import isWorker
from datetime import datetime, timedelta


def inline(update: Update, context):
    user_id = update.callback_query.from_user.id
    worker = getWorker(user_id)
    step = Data.objects.get(telegram_id=user_id).data
    data = update.callback_query.data.split("_")
    # print(data)
    if isWorker(user_id):
        if len(data) == 2 and data[0] == 'sendBoss':
            update.callback_query.message.edit_reply_markup()
            req = Request_price.objects.get(pk=data[1])
            total = req.workers.first()
            staff = total.full_name
            text = getAvansText(name=staff.full_name, req=req, month=req.month, salary=total.itog_1, money=req.price,
                                balance=total.ostatok_1 + req.price)
            context.bot.send_message(chat_id=worker.boss.telegram_id, text=text, parse_mode='HTML',
                                     reply_markup=acceptInlineButton(req.pk))
        elif len(data) == 2 and data[0] == 'done':
            update.callback_query.message.edit_reply_markup()
            req = Request_price.objects.get(pk=data[1])
            req.status = Request_price.Status.ACCEPTED
            req.save()
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
        elif data[0] == 'room':
            room = Rooms.objects.get(pk=data[1])
            today = datetime.now().date()
            if len(data) == 2:
                next_date = today + timedelta(days=1)
                text = roomTableText(room, today)
                update.callback_query.edit_message_text(text=text, parse_mode='HTML',
                                                        reply_markup=roomMenuButton(room=room, date=today,
                                                                                    next_date=next_date))
            elif data[-1] == 'home':
                rooms = Rooms.objects.filter(is_active=True)
                update.callback_query.edit_message_text(text="Xonani tanlang", parse_mode='HTML',
                                                        reply_markup=roomListInlineButton(rooms=rooms))
            elif 'book' in data:
                date = datetime.strptime(data[2], "%Y-%m-%d").date()
                step.update({"room": data[1], "book_date": data[2]})
                Data.objects.filter(telegram_id=user_id).update(data=step)
                text = roomTableText(room, date)
                text += "Boshlanish vaqtini tanlang"
                hours = freeRoomHours(room, date)
                update.callback_query.edit_message_text(text=text, parse_mode='HTML',
                                                        reply_markup=freeRoomHoursInlineButton(room, hours))
            elif 'next' in data:
                date = datetime.strptime(data[2], "%Y-%m-%d").date()
                prev_date = date - timedelta(days=1)
                next_date = date + timedelta(days=1)
                text = roomTableText(room, date)
                update.callback_query.edit_message_text(text=text, parse_mode='HTML',
                                                        reply_markup=roomMenuButton(room=room, date=date,
                                                                                    prev_date=prev_date,
                                                                                    next_date=next_date))
            elif 'prev' in data:
                date = datetime.strptime(data[2], "%Y-%m-%d").date()
                next_date = date + timedelta(days=1)
                prev_date = date - timedelta(days=1)
                if prev_date >= today:
                    button = roomMenuButton(room=room, date=date, prev_date=prev_date, next_date=next_date)
                else:
                    button = roomMenuButton(room=room, date=date, next_date=next_date)
                text = roomTableText(room, date)
                update.callback_query.edit_message_text(text=text, parse_mode='HTML',
                                                        reply_markup=button)

            elif 'start' in data:
                date = datetime.strptime(step.get('book_date'), "%Y-%m-%d").date()
                step.update({"start_time": data[2]})
                Data.objects.filter(telegram_id=user_id).update(data=step)
                text = roomTableText(room, date)
                text += "Tugash vaqtini tanlang"
                hours = freeRoomEndHours(room, date, int(data[2]))
                update.callback_query.edit_message_text(text=text, parse_mode='HTML',
                                                        reply_markup=freeRoomHoursInlineButton(room, hours, "end"))
            elif 'end' in data:
                user = getWorker(user_id)
                date = datetime.strptime(step.get('book_date'), "%Y-%m-%d").date()
                start_time = datetime.strptime(step.get('start_time'), "%H").time()
                end_time = datetime.strptime(data[2], "%H").time()
                next_date = date + timedelta(days=1)
                prev_date = date - timedelta(days=1)
                step.update({"step": 0, "end_time": data[2]})
                event = step.get('event')
                Data.objects.filter(telegram_id=user_id).update(data=step)
                selectBookTime(user=user, room=room, event=event, date=date, start_time=start_time, end_time=end_time)
                text = roomTableText(room, date)
                if prev_date >= today:
                    button = roomMenuButton(room=room, date=date, prev_date=prev_date, next_date=next_date)
                else:
                    button = roomMenuButton(room=room, date=date, next_date=next_date)
                update.callback_query.edit_message_text(text=text, parse_mode='HTML', reply_markup=None)
                context.bot.send_message(chat_id=user_id, text="Xona bron qilindi", reply_markup=avansButton(True))
                send_message_to_group(context, text)
