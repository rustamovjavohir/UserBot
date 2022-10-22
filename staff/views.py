from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update

from config.settings import URL_1C, PASSWORD_1C, LOGIN_1C
from .buttons import avansButton, homeButton, acceptButton, acceptInlineButton
from .models import *
import requests
from telegram.ext import CallbackContext
import datetime
from dateutil.relativedelta import relativedelta
from .utils import checkMoney, checkNextMonth, splitMoney, checkNextMonthMoney, getWorker, isITStaff


def isWorker(telegram_id) -> bool:
    have = Workers.objects.filter(telegram_id=telegram_id, active=True).exists() or \
           InfTech.objects.filter(telegram_id=telegram_id, active=True).exists()
    return have


def inform(user_id):
    worker = getWorker(user_id)
    text = f"<strong>F.I.O.:</strong> {worker.full_name}\n"
    if type(worker.department) is str:
        text += f"<strong>Bo'lim:</strong> {worker.department}\n"
    else:
        text += f"<strong>Bo'lim:</strong> {worker.department.name}\n"
    text += f"<strong>Ish:</strong> {worker.job}\n"
    text += f"<strong>Telefon raqam:</strong> {worker.phone}\n"
    text += f"<strong>Telegram ID:</strong> {worker.telegram_id}\n"
    return text


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if isWorker(telegram_id=user_id):
        update.message.reply_html(inform(user_id), reply_markup=avansButton())
        worker = getWorker(user_id, True)
        obj, created = Data.objects.get_or_create(telegram_id=user_id)
        obj.telegram_id = user_id
        obj.data = {"step": 0, "name": worker.full_name}
        obj.save()
    else:
        update.message.reply_text(f"ID: {user_id}")


#################################################################################################################


def order(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    if isWorker(user_id):
        if step["step"] == 0 and msg == 'Avans so`rovi':
            step.update({"step": 1})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            update.message.reply_text('Avans miqdorini yozing',
                                      reply_markup=homeButton())
        elif step["step"] == 1 and msg != '🏠Bosh sahifa':
            if msg.isnumeric():
                if checkMoney(user_id=user_id, money=int(msg)) or isITStaff(user_id):
                    step.update({"step": 2, "price": int(msg)})
                    Data.objects.filter(telegram_id=user_id).update(data=step)
                    text = f"<strong>Sana:</strong> {datetime.datetime.now().strftime('%d.%m.%Y')}\n"
                    text += f"<strong>F.I.O.:</strong> {step['name']}\n"
                    text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(step['price'])} So`m\n"
                    update.message.reply_html(text, reply_markup=acceptButton())
                else:
                    months = getMonthList()
                    next_month = datetime.date.today() + relativedelta(months=+1)
                    step.update({"step": 0})
                    Data.objects.filter(telegram_id=user_id).update(data=step)
                    if checkNextMonth(user_id):
                        if checkNextMonthMoney(user_id) == 0:
                            text = f"Bo'ldida endi, <strong>{months[next_month.month - 1]}</strong> ni " \
                                   f"oyliginiyam olib bo'ldiz🤌.\n" \
                                   f"Izoh: Eng ko'pi bilan 2 oy uchun avans olsa bo'ladi"
                        else:
                            text = f"Ishtaha karnakku, {months[next_month.month - 1]} nikiniyam qo'shsa ham yetmayapdi🙅🏻‍♂.\n" \
                                   f"<strong>Izoh</strong>: Yozilgan summa 2 oylik avans pulidan ko'p"
                    else:
                        text = f"Boshliq oylik yozmabdilaku🤲. \n" \
                               f"Izoh:<strong> {months[next_month.month - 1]}</strong> uchun oylik kiritilmagan"
                    update.message.reply_html(text, reply_markup=avansButton())
            else:
                update.message.reply_text('❗️❗️❗️Probelsiz faqat raqam kiriting',
                                          reply_markup=homeButton())
        elif step["step"] == 2 and msg == "✅So`rovni tasdiqlayman":
            months = getMonthList()
            if isITStaff(user_id):
                price = int(step['price'])
                req1 = Request_price.objects.create(price=price, avans=True, month=months[datetime.date.today().month - 1],
                                                   department_id='АЙТи отдел', is_deleted=True)
                req = ITRequestPrice.objects.create(price=price, avans=True, secondId=req1.pk,
                                                    month=months[datetime.date.today().month - 1],
                                                    department_id='АЙТи отдел')
                text = f"<strong>ID:</strong> {req.secondId}\n"
                text += f"<strong>Sana:</strong> {datetime.datetime.now().strftime('%d.%m.%Y')}\n"
                text += f"<strong>F.I.O.:</strong> {step['name']}\n"
                text += f"<strong>Oy: {months[datetime.date.today().month - 1]}</strong>\n"
                text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(price)} So`m\n"

                worker = getWorker(user_id)
                req.workers.add(worker)
                context.bot.send_message(chat_id=InfTech.objects.filter(is_boss=True).first().telegram_id,
                                         text=text, parse_mode="html",
                                         reply_markup=acceptInlineButton(req.secondId))
                update.message.reply_text(f"✅So`rov bo`lim boshlig`iga yuborildi, ID: {req.secondId}")
                update.message.reply_text("Bosh sahifa", reply_markup=avansButton())
            elif getattr(getWorker(user_id), 'is_boss'):
                print("salom")
                update.message.reply_html("Bosh sahifa",
                                          reply_markup=avansButton())
                req = Request_price.objects.create(price=step['price'], avans=True,
                                                   department_id=Workers.objects.get(
                                                       telegram_id=user_id).department.ids)
                obj = Total.objects.get(full_name__telegram_id=user_id,
                                        year=datetime.datetime.now().year,
                                        month=months[int(datetime.datetime.now().month) - 1])
                req.workers.add(obj)
                url = f"{URL_1C}ut3/hs/create_applications"

                # auth = ("django_admin", "DJango_96547456")
                auth = (LOGIN_1C, PASSWORD_1C)
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
                avans_month = months[int(datetime.datetime.now().month) - 1]
                price = int(step['price'])
                money_split = splitMoney(user_id=user_id, money=price)
                for month, money in money_split:
                    if money == 0:
                        continue
                    req = Request_price.objects.create(price=money, avans=True, month=months[month - 1],
                                                       department_id=Workers.objects.get(
                                                           telegram_id=user_id).department.ids)

                    obj = Total.objects.get(full_name__telegram_id=user_id,
                                            year=datetime.datetime.now().year,
                                            month=avans_month)
                    req.workers.add(obj)
                    step.update({"step": 0})
                    Data.objects.filter(telegram_id=user_id).update(data=step)
                    update.message.reply_text(f"✅So`rov bo`lim boshlig`iga yuborildi, ID: {req.id}")
                    boss = Workers.objects.filter(is_boss=True,
                                                  department=Workers.objects.get(telegram_id=user_id).department)
                    text = f"<strong>ID:</strong> {req.pk}\n"
                    text += f"<strong>Sana:</strong> {datetime.datetime.now().strftime('%d.%m.%Y')}\n"
                    text += f"<strong>F.I.O.:</strong> {step['name']}\n"
                    text += f"<strong>Oy: {months[month - 1]}</strong>\n"
                    text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(money)} So`m\n"
                    context.bot.send_message(chat_id=boss[0].telegram_id, text=text, parse_mode="html",
                                             reply_markup=acceptInlineButton(req.id))
                update.message.reply_text("Bosh sahifa",
                                          reply_markup=avansButton())
        elif msg == '🏠Bosh sahifa':
            step.update({"step": 0})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            update.message.reply_html("Bosh sahifa",
                                      reply_markup=avansButton())
