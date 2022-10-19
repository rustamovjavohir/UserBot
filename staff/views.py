from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update

from config.settings import URL_1C
from .models import *
import requests
from telegram.ext import CallbackContext
import datetime


def inform(user_id):
    worker = Workers.objects.get(telegram_id=user_id)
    text = f"<strong>F.I.O.:</strong> {worker.full_name}\n"
    text += f"<strong>Bo'lim:</strong> {worker.department.name}\n"
    text += f"<strong>Ish:</strong> {worker.job}\n"
    text += f"<strong>Telefon raqam:</strong> {worker.phone}\n"
    text += f"<strong>Telegram ID:</strong> {worker.telegram_id}\n"
    return text


def list_workers():
    workers = Workers.objects.filter(active=True)
    ids = []
    for i in workers:
        ids.append(i.telegram_id)
    return ids


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in list_workers():
        update.message.reply_html(inform(user_id), reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Avans so`rovi')]],
                                                                                    resize_keyboard=True,
                                                                                    one_time_keyboard=True))
        worker = Workers.objects.get(telegram_id=user_id)
        try:
            a = Data.objects.get(telegram_id=user_id)
            Data.objects.filter(telegram_id=user_id).update(data={"step": 0, "name": worker.full_name})
        except:
            Data.objects.create(telegram_id=user_id, data={"step": 0, "name": worker.full_name})
    else:
        update.message.reply_text(f"ID: {user_id}")

    #################################################################################################################


def order(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    if user_id in list_workers():
        if step["step"] == 0 and msg == 'Avans so`rovi':
            step.update({"step": 1})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            update.message.reply_text('Avans miqdorini yozing',
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton('🏠Bosh sahifa')]],
                                                                       resize_keyboard=True, one_time_keyboard=True))
        elif step["step"] == 1 and msg != '🏠Bosh sahifa':
            if msg.isnumeric():
                step.update({"step": 2, "price": int(msg)})
                Data.objects.filter(telegram_id=user_id).update(data=step)
                text = f"<strong>Sana:</strong> {datetime.datetime.now().strftime('%d.%m.%Y')}\n"
                text += f"<strong>F.I.O.:</strong> {step['name']}\n"
                text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(step['price'])} So`m\n"
                update.message.reply_html(text,
                                          reply_markup=ReplyKeyboardMarkup([[KeyboardButton('✅So`rovni tasdiqlayman')],
                                                                            [KeyboardButton('🏠Bosh sahifa')]],
                                                                           resize_keyboard=True,
                                                                           one_time_keyboard=True))
            else:
                update.message.reply_text('❗️❗️❗️Probelsiz faqat raqam kiriting',
                                          reply_markup=ReplyKeyboardMarkup([[KeyboardButton('🏠Bosh sahifa')]],
                                                                           resize_keyboard=True,
                                                                           one_time_keyboard=True))
        elif step["step"] == 2 and msg == "✅So`rovni tasdiqlayman":
            if Workers.objects.get(telegram_id=user_id).is_boss:
                update.message.reply_html("Bosh sahifa",
                                          reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Avans so`rovi')]],
                                                                           resize_keyboard=True,
                                                                           one_time_keyboard=True))
                req = Request_price.objects.create(price=step['price'], avans=True,
                                                   department_id=Workers.objects.get(
                                                       telegram_id=user_id).department.ids)
                months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
                          "Ноябрь", "Декабрь"]
                obj = Total.objects.get(full_name=Workers.objects.get(telegram_id=user_id),
                                        year=datetime.datetime.now().year,
                                        month=months[int(datetime.datetime.now().month) - 1])
                req.workers.add(obj)
                url = f"{URL_1C}ut3/hs/create_applications"
                auth = ("django_admin", "DJango_96547456")
                js = {
                    "id": str(req.pk),
                    "department": req.department_id,
                    "price": req.price,
                    "avans": True,
                    "comment": ""
                }
                res = requests.post(url=url, auth=auth, json=js)
                step.update({"step": 0})
                Data.objects.filter(telegram_id=user_id).update(data=step)
                if 'success' in list(res.json().keys()):
                    update.message.reply_html(f"✅So`rov tasdiqlandi, kassaga chiqishingiz mumkin ID: {req.pk}")
                else:
                    update.message.reply_html("🚫Xatolik yuz berdi")

            else:
                req = Request_price.objects.create(price=step['price'], avans=True,
                                                   department_id=Workers.objects.get(
                                                       telegram_id=user_id).department.ids)
                months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
                          "Ноябрь", "Декабрь"]

                obj = Total.objects.get(full_name=Workers.objects.get(telegram_id=user_id),
                                        year=datetime.datetime.now().year,
                                        month=months[int(datetime.datetime.now().month) - 1])
                req.workers.add(obj)
                step.update({"step": 0})
                Data.objects.filter(telegram_id=user_id).update(data=step)
                update.message.reply_text(f"✅So`rov bo`lim boshlig`iga yuborildi, ID: {req.id}")
                update.message.reply_text("Bosh sahifa",
                                          reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Avans so`rovi')]],
                                                                           resize_keyboard=True,
                                                                           one_time_keyboard=True))
                boss = Workers.objects.filter(is_boss=True,
                                              department=Workers.objects.get(telegram_id=user_id).department)
                text = f"<strong>ID:</strong> {req.pk}\n"
                text += f"<strong>Sana:</strong> {datetime.datetime.now().strftime('%d.%m.%Y')}\n"
                text += f"<strong>F.I.O.:</strong> {step['name']}\n"
                text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(step['price'])} So`m\n"
                context.bot.send_message(chat_id=boss[0].telegram_id, text=text, parse_mode="html",
                                         reply_markup=InlineKeyboardMarkup(
                                             [[InlineKeyboardButton("✅Tasdiqlash", callback_data=f"done_{req.id}")],
                                              [InlineKeyboardButton("❌Rad etish", callback_data=f"not_{req.id}")]]
                                         ))
        elif msg == '🏠Bosh sahifa':
            step.update({"step": 0})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            update.message.reply_html("Bosh sahifa",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Avans so`rovi')]],
                                                                       resize_keyboard=True,
                                                                       one_time_keyboard=True))


def inline(update: Update, context):
    user_id = update.callback_query.from_user.id
    data = update.callback_query.data.split("_")
    if user_id in list_workers():
        if len(data) == 2 and data[0] == 'done':
            update.callback_query.message.edit_reply_markup()
            req = Request_price.objects.get(pk=data[1])
            url = f"{URL_1C}ut3/hs/create_applications"
            auth = ("django_admin", "DJango_96547456")
            js = {
                "id": str(req.pk),
                "department": req.department_id,
                "price": req.price,
                "avans": True,
                "comment": ""
            }
            res = requests.post(url=url, auth=auth, json=js)
            if 'success' in list(res.json().keys()):
                update.callback_query.message.reply_text("✅So`rov kassaga yuborildi")
                for i in req.workers.all():
                    context.bot.send_message(chat_id=i.full_name.telegram_id,
                                             text=f"✅So`rov tasdiqlandi, kassaga chiqishingiz mumkin ID: {req.pk}")
            else:
                update.callback_query.message.reply_text("🚫Xatolik yuz berdi")
        elif len(data) == 2 and data[0] == 'not':
            update.callback_query.message.edit_reply_markup()
            req = Request_price.objects.get(pk=data[1])
            for i in req.workers.all():
                context.bot.send_message(chat_id=i.full_name.telegram_id,
                                         text=f"❌So`rov bo`lim boshlig`i tomonidan rad etildi, ID: {req.pk}")
            Request_price.objects.get(pk=data[1]).delete()
            update.callback_query.message.reply_text("❌So`rov rad etildi")
