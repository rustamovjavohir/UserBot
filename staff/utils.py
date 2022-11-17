import threading

import requests
from telegram.ext import CallbackContext

from staff.buttons import *
from staff.models import *
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from telegram import Bot, Update
from config.settings import S_TOKEN, URL_1C, LOGIN_1C, PASSWORD_1C

bot = Bot(token=S_TOKEN)


def checkReceivedSalary(user_id, month=""):
    if not month:
        months = getMonthList()
        month = months[(date.today() + relativedelta(months=-2)).month]
    is_received = Request_price.objects.filter(avans=False, answer=False, month=month,
                                               workers__full_name__telegram_id=user_id).exists()
    return is_received


def checkMoney(user_id, money: int) -> bool:
    sum_money = 0
    total = Total.objects.filter(full_name__telegram_id=user_id).order_by('-id')[0:2]
    for item in total:
        sum_money += item.ostatok_1
    if sum_money >= money:
        return True
    return False


def checkNextMonth(user_id) -> bool:
    next_month = date.today() + relativedelta(months=+1)
    months = getMonthList()
    if Total.objects.filter(full_name__telegram_id=user_id, year=next_month.year,
                            month=months[next_month.month - 1]).exists():
        return True
    return False


def checkNextMonthMoney(user_id) -> int:
    next_month = date.today() + relativedelta(months=+1)
    months = getMonthList()
    if checkNextMonth(user_id):
        next_month_money = Total.objects.filter(full_name__telegram_id=user_id, year=next_month.year,
                                                month=months[next_month.month - 1]).first()
        return next_month_money.ostatok_1
    return 0


def splitMoney(user_id, money: int) -> tuple:
    """
    ((this_month, first_money), (next_month, second_money))
    """
    total_all = Total.objects.filter(full_name__telegram_id=user_id).order_by('-id')[1:2].first()
    current_day = datetime(int(total_all.year), int(total_all.month_index), 1)
    next_month = nextMonth(total_all)
    print(total_all.ostatok_1)
    if total_all.ostatok_1 >= money:
        return (total_all.month_index, money), (0, 0)
    elif total_all.ostatok_1 == 0:
        return (next_month.month, money), (0, 0)
    elif 0 < total_all.ostatok_1 < money:
        return (current_day.month, total_all.ostatok_1), (next_month.month, abs(money - total_all.ostatok_1))
    # total_1 manfiy bulishi mumkin
    print(f"xato{datetime.datetime.now()}")
    return 0, 0


def getWorker(user_id, active=True):
    worker = Workers.objects.filter(telegram_id=user_id, active=active).first()
    if not worker:
        worker = InfTech.objects.filter(telegram_id=user_id, active=active).first()
    return worker


def isITStaff(user_id):
    return InfTech.objects.filter(telegram_id=user_id, active=True).first()


def sendNotification(notifications, workers):
    for item in notifications:
        for worker in workers:
            try:
                bot.send_message(chat_id=worker.telegram_id, text=item.text)
            except:
                pass


def getTotalList(user_id):
    totals = [total for total in Total.objects.filter(full_name__telegram_id=user_id) if total.ostatok_1.__ge__(0)]
    return totals


def getFirstTotal(user_id):
    totals = getTotalList(user_id)
    return totals[0]


def nextMonth(obj):
    current_day = datetime(int(getattr(obj, "year")), int(getattr(obj, "month_index")), 1)
    next_month = current_day + relativedelta(months=+1)
    return next_month


def getReportTotalText(total: Total):
    text = f"<strong>F.I.O: </strong>{total.full_name.full_name}\n" \
           f"<strong>Oy: </strong>{total.month}\n" \
           f"<strong>Bonus: </strong>{total.bonuss}\n" \
           f"<strong>Jarima: </strong>{total.paid}\n" \
           f"<strong>Jami: </strong>{total.itog}\n" \
           f"<strong>To'landi: </strong>{total.vplacheno}\n" \
           f"<strong>Qoldiq: </strong>{total.ostatok}\n"
    return text


def getAvansText(name, req, month, money):
    months = getMonthList()
    text = f"<strong>ID:</strong> {req.pk}\n"
    text += f"<strong>Sana:</strong> {datetime.now().strftime('%d.%m.%Y')}\n"
    text += f"<strong>F.I.O.:</strong> {name}\n"
    text += f"<strong>Oy: {months[month - 1]}</strong>\n"
    text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(money)} So`m\n"

    return text


def notificationBot(message, workers: Workers = 0, info_staff: InfTech = 0, is_all=True, **kwargs):
    if is_all:
        workers = Workers.objects.filter(active=True)
        info_staff = InfTech.objects.filter(active=True)
    for staff in info_staff:
        try:
            bot.send_message(chat_id=staff.telegram_id, text=message, parse_mode="HTML")
        except:
            pass
    for worker in workers:
        try:
            bot.send_message(chat_id=worker.telegram_id, text=message, parse_mode="HTML")
        except:
            pass
    return 1


def isWorker(telegram_id) -> bool:
    have = Workers.objects.filter(telegram_id=telegram_id, active=True).exists() or \
           InfTech.objects.filter(telegram_id=telegram_id, active=True).exists()
    return have


def isKitchen(user_id) -> bool:
    if isWorker(user_id):
        return getWorker(user_id).job.__eq__('уборщица')
    return False


def isCashier(user_id) -> bool:
    if isWorker(user_id):
        return getWorker(user_id).department.ids.__eq__("00-000041")
    return False


def requestAvans(update: Update, context: CallbackContext, step_count=1, is_self=True):
    step_dict = {"step": step_count}
    if not is_self:
        msg = update.message.text
        worker = Workers.objects.filter(full_name=msg).first()
        step_dict = {"step": step_count, "other_staff_id": worker.telegram_id}
    user_id = update.message.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    step.update(step_dict)
    Data.objects.filter(telegram_id=user_id).update(data=step)
    update.message.reply_text('Avans miqdorini yozing',
                              reply_markup=homeButton())


def setAvans(update: Update, context: CallbackContext, worker_id=None, menu_button=None):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    step_num = 6
    staff_name = getWorker(step.get("other_staff_id", user_id)).full_name
    if menu_button is None:
        menu_button = avansButton()
    if worker_id is None:
        staff_name = step['name']
        step_num = 2
        worker_id = user_id
    if msg.isnumeric():
        if (checkMoney(user_id=worker_id, money=int(msg)) or isITStaff(worker_id)) \
                and not checkReceivedSalary(worker_id):
            step.update({"step": step_num, "price": int(msg)})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            text = f"<strong>Sana:</strong> {datetime.now().strftime('%d.%m.%Y')}\n"
            text += f"<strong>F.I.O.:</strong> {staff_name}\n"
            text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(step['price'])} So`m\n"
            update.message.reply_html(text, reply_markup=acceptButton())
        else:
            months = getMonthList()
            total_all = getFirstTotal(user_id=worker_id)
            next_month = nextMonth(total_all)
            step.update({"step": 0})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            if checkNextMonth(worker_id):
                if checkNextMonthMoney(worker_id) == 0:
                    text = f"Bo'ldida endi, <strong>{months[next_month.month - 1]}</strong> ni " \
                           f"oyliginiyam olib bo'ldiz🤌.\n" \
                           f"Izoh: Eng ko'pi bilan 2 oy uchun avans olsa bo'ladi"
                else:
                    text = f"Ishtaha karnakku, {months[next_month.month - 1]} nikiniyam qo'shsa ham yetmayapdi🙅🏻‍♂.\n" \
                           f"<strong>Izoh</strong>: Yozilgan summa 2 oylik avans pulidan ko'p"
            else:
                text = f"Boshliq oylik yozmabdilaku🤲. \n" \
                       f"Izoh:<strong> {months[next_month.month - 1]}</strong> uchun oylik kiritilmagan"
            update.message.reply_html(text, reply_markup=menu_button)
    else:
        update.message.reply_text('❗️❗️❗️Probelsiz faqat raqam kiriting',
                                  reply_markup=homeButton())


def applyAvans(update: Update, context: CallbackContext, worker_id=None):
    user_id = update.message.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    staff_name = getWorker(step.get("other_staff_id", user_id)).full_name
    if not worker_id:
        worker_id = user_id
    months = getMonthList()
    if isITStaff(worker_id):
        price = int(step['price'])
        req1 = Request_price.objects.create(price=price, avans=True,
                                            month=months[date.today().month - 1],
                                            department_id='АЙТи отдел', is_deleted=True)
        req = ITRequestPrice.objects.create(price=price, avans=True, secondId=req1.pk,
                                            month=months[date.today().month - 1],
                                            department_id='АЙТи отдел')
        text = f"<strong>ID:</strong> {req.secondId}\n"
        text += f"<strong>Sana:</strong> {datetime.now().strftime('%d.%m.%Y')}\n"
        text += f"<strong>F.I.O.:</strong> {staff_name}\n"
        text += f"<strong>Oy: {months[date.today().month - 1]}</strong>\n"
        text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(price)} So`m\n"

        worker = getWorker(worker_id)
        req.workers.add(worker)
        context.bot.send_message(chat_id=InfTech.objects.filter(is_boss=True).first().telegram_id,
                                 text=text, parse_mode="html",
                                 reply_markup=acceptInlineButton(req.secondId))
        step.update({"step": 0})
        Data.objects.filter(telegram_id=worker_id).update(data=step)
        update.message.reply_text(f"✅So`rov bo`lim boshlig`iga yuborildi, ID: {req.secondId}")
        update.message.reply_text("Bosh sahifa", reply_markup=avansButton())
    elif getattr(getWorker(worker_id), 'is_boss'):
        update.message.reply_html("Bosh sahifa",
                                  reply_markup=avansButton())
        price = int(step['price'])
        money_split = splitMoney(user_id=worker_id, money=price)
        for month, money in money_split:
            if money == 0:
                continue
            req = Request_price.objects.create(price=money, avans=True, month=months[month - 1],
                                               department_id=Workers.objects.get(
                                                   telegram_id=worker_id).department.ids)
            try:
                obj = Total.objects.get(full_name__telegram_id=worker_id,
                                        year=datetime.now().year,
                                        month=months[month - 1])
                req.workers.add(obj)
            except Exception as ex:
                print(ex)
            staff = getWorker(worker_id)
            if staff.boss:
                text = getAvansText(name=staff.full_name, req=req, month=month, money=money)
                context.bot.send_message(chat_id=staff.boss.telegram_id, text=text, parse_mode="html",
                                         reply_markup=acceptInlineButton(req.id))
                update.message.reply_text(text=f"✅So`rov {staff.boss.full_name}ga yuborildi, ID:  {req.pk}")
            else:
                url = f"{URL_1C}ut3/hs/radius_bot/create_applications"
                auth = (LOGIN_1C, PASSWORD_1C)
                js = {
                    "id": str(req.pk),
                    "department": req.department_id,
                    "price": req.price,
                    "avans": True,
                    "comment": ""
                }
                res = requests.post(url=url, auth=auth, json=js)
                if 'success' in list(res.json().keys()):
                    update.message.reply_html(f"✅So`rov tasdiqlandi, kassaga chiqishingiz mumkin ID: {req.pk}")
                else:
                    update.message.reply_html("🚫Xatolik yuz berdi")
        step.update({"step": 0})
        Data.objects.filter(telegram_id=worker_id).update(data=step)
        update.message.reply_text("Bosh sahifa", reply_markup=avansButton())

    else:
        price = int(step['price'])
        money_split = splitMoney(user_id=worker_id, money=price)
        for month, money in money_split:
            if money == 0:
                continue
            req = Request_price.objects.create(price=money, avans=True, month=months[month - 1],
                                               department_id=Workers.objects.get(
                                                   telegram_id=worker_id).department.ids)
            try:
                obj = Total.objects.get(full_name__telegram_id=worker_id,
                                        year=datetime.now().year,
                                        month=months[month - 1])
                req.workers.add(obj)
            except Exception as ex:
                print(ex)
            step.update({"step": 0})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            update.message.reply_text(f"✅So`rov bo`lim boshlig`iga yuborildi, ID: {req.id}")
            boss = Workers.objects.filter(is_boss=True,
                                          department=Workers.objects.get(telegram_id=worker_id).department).first()
            text = getAvansText(name=staff_name, req=req, month=month, money=money)
            context.bot.send_message(chat_id=boss.telegram_id, text=text, parse_mode="html",
                                     reply_markup=acceptInlineButton(req.id))
        reply_markup = avansButton()
        if isCashier(user_id):
            reply_markup = cashierButton()
        update.message.reply_text("Bosh sahifa", reply_markup=reply_markup)


def report(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    if not isITStaff(user_id):
        for total in getTotalList(user_id):
            text = getReportTotalText(total)
            context.bot.send_message(chat_id=user_id, text=text, parse_mode="HTML",
                                     reply_markup=homeButton())

        step["step"] = 3
        Data.objects.filter(telegram_id=user_id).update(data=step)
    else:
        text = "Biz boshqa respublika 😂"
        context.bot.send_message(chat_id=user_id, text=text, parse_mode="HTML",
                                 reply_markup=homeButton())


def home(update: Update, context: CallbackContext, menu_button=None):
    if menu_button is None:
        menu_button = avansButton()
    user_id = update.message.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    step.update({"step": 0})
    Data.objects.filter(telegram_id=user_id).update(data=step)
    update.message.reply_html("Bosh sahifa",
                              reply_markup=menu_button)


def createAvans(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    step.update({"step": 3})
    Data.objects.filter(telegram_id=user_id).update(data=step)
    update.message.reply_html("Hodimning ismini kiriting (фақат кирил ҳарфларида)",
                              reply_markup=homeButton())


def filterWorkers(message, user_id):
    return Workers.objects.filter(full_name__icontains=message, active=True)


def selectWorker(user_id, update: Update, context: CallbackContext):
    step = Data.objects.get(telegram_id=user_id).data
    step.update({"step": 4})
    Data.objects.filter(telegram_id=user_id).update(data=step)
    msg = update.message.text
    workers = filterWorkers(msg, user_id)
    context.bot.send_message(chat_id=user_id, text="Ishchini tanlang", reply_markup=workersListButton(workers))
