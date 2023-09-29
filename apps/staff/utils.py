from time import sleep

import requests
from telegram.ext import CallbackContext

from apps.rooms.models import Rooms, Timetable
from apps.staff.buttons import *
from dateutil.relativedelta import relativedelta
from telegram import Bot, Update

from apps.staff.models import *
from apps.staff.tasks import create_auto_delete_req
from config.settings import S_TOKEN, URL_1C, LOGIN_1C, PASSWORD_1C, GROUP_ID
from datetime import datetime, date

bot = Bot(token=S_TOKEN)


def sortedByMonthIndex(iterable, reverse=True):
    return sorted(iterable, key=lambda t: (t.year, t.month_index), reverse=reverse)


def checkReceivedSalary(user_id, month=""):
    if not month:
        months = getMonthList()
        month = months[(date.today() + relativedelta(months=-2)).month % 12]
    is_received = Request_price.objects.filter(avans=False, answer=False, month=month,
                                               workers__full_name__telegram_id=user_id).exists()
    return is_received


def checkMoney(user_id, money: int) -> bool:
    sum_money = 0
    # total = Total.objects.filter(full_name__telegram_id=user_id).order_by('-id')[0:2]
    total = Total.objects.filter(full_name__telegram_id=user_id)
    total = sortedByMonthIndex(total)[0:2]
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
    # total_all = Total.objects.filter(full_name__telegram_id=user_id).order_by('-id')[1:2].first()
    total_all = Total.objects.filter(full_name__telegram_id=user_id)
    try:
        total_all = sortedByMonthIndex(total_all)[1]
    except IndexError:
        # total_all = Total.objects.filter(full_name__telegram_id=user_id)
        total_all = sortedByMonthIndex(total_all)[0]
    current_day = datetime(int(total_all.year), int(total_all.month_index), 1)
    next_month = nextMonth(total_all)
    if total_all.ostatok_1 >= money:
        return (total_all.month_index, money), (0, 0)
    elif total_all.ostatok_1 == 0:
        return (next_month.month, money), (0, 0)
    elif 0 < total_all.ostatok_1 < money:
        return (current_day.month, total_all.ostatok_1), (next_month.month, abs(money - total_all.ostatok_1))
    # total_1 manfiy bulishi mumkin
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
    total_list = []
    totals = Total.objects.filter(full_name__telegram_id=user_id).order_by('id')
    for total in totals:
        if total.ostatok_1.__ge__(0):
            total_list.append(total)

    # totals = [total for total in Total.objects.filter(full_name__telegram_id=user_id).order_by('id') if
    #           total.ostatok_1.__ge__(0)]
    return total_list


def getFirstTotal(user_id):
    totals = getTotalList(user_id)
    return totals[-1]


def nextMonth(obj):
    current_day = datetime(int(getattr(obj, "year")), int(getattr(obj, "month_index")), 1)
    next_month = current_day + relativedelta(months=+1)
    return next_month


def getAvansText(name, req, month, salary, money, balance):
    text = f"<strong>ID:</strong> {req.pk}\n"
    text += f"<strong>Sana:</strong> {datetime.now().strftime('%d.%m.%Y')}\n"
    text += f"<strong>F.I.O.:</strong> {name}\n"
    text += f"<strong>Oy: {month}</strong>\n"
    text += f"<strong>Oylik:</strong> {'{:,}'.format(salary)} So`m\n"
    text += f"<strong>Avans miqdori:</strong> {'{:,}'.format(money)} So`m\n" \
            f"<strong>Balans:</strong> {'{:,}'.format(balance)} So`m\n"

    if balance <= salary * 0.3 or money >= salary * 0.7:
        text += f"\n<strong>⚠️Diqqat!</strong> Oylikning 70% dan ortiq miqdorda avans berilmoqda!\n"
    return text


def getReportTotalText(total: Total):
    text = f"<strong>F.I.O: </strong>{total.full_name.full_name}\n" \
           f"<strong>Oy: </strong>{total.month}\n" \
           f"<strong>Bonus: </strong>{total.bonuss}\n" \
           f"<strong>Jarima: </strong>{total.paid}\n" \
           f"<strong>Jami: </strong>{total.itog}\n" \
           f"<strong>To'landi: </strong>{total.vplacheno}\n" \
           f"<strong>Qoldiq: </strong>{total.ostatok}\n"
    return text


def notificationBot(message, workers: Workers = 0, info_staff: InfTech = 0, is_all=True, is_office=True, **kwargs):
    if is_all:
        workers = Workers.objects.filter(active=True, in_office=is_office)
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
        # return getWorker(user_id).department.ids.__eq__("00-000023")
    return False


def hasPermBookRoom(user_id) -> bool:
    if isWorker(user_id):
        return getWorker(user_id).in_office
    # getWorker(user_id).role in [Workers.Role.ADMIN, Workers.Role.SUPER_ADMIN, Workers.Role.ADMINISTRATOR])
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
        menu_button = avansButton(hasPermBookRoom(user_id))
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
        update.message.reply_text("Bosh sahifa", reply_markup=avansButton(hasPermBookRoom(user_id)))
    elif getattr(getWorker(worker_id), 'is_boss'):
        price = int(step['price'])
        money_split = splitMoney(user_id=worker_id, money=price)
        for month, money in money_split:
            if money == 0:
                continue
            req = Request_price.objects.create(price=money, avans=True, month=months[month - 1],
                                               status=Request_price.Status.ACCEPTED,
                                               department_id=Workers.objects.get(telegram_id=worker_id).department.ids)
            try:
                obj = Total.objects.get(full_name__telegram_id=worker_id,
                                        year__in=[datetime.now().year - 1, datetime.now().year],
                                        month=months[month - 1])
                req.workers.add(obj)
            except Exception as ex:
                print(ex)
            staff = getWorker(worker_id)
            if staff.boss:
                text = getAvansText(name=staff.full_name, req=req, salary=obj.itog_1, month=months[month - 1],
                                    money=money,
                                    balance=obj.ostatok_1 + money)
                context.bot.send_message(chat_id=staff.boss.telegram_id, text=text, parse_mode="html",
                                         reply_markup=acceptInlineButton(req.id))
                update.message.reply_text(text=f"✅So`rov {staff.boss.full_name}ga yuborildi, ID:  {req.pk}")
            else:
                url = f"{URL_1C}hs/radius_bot/create_applications"
                auth = (LOGIN_1C, PASSWORD_1C)
                js = {
                    "id": str(req.pk),
                    "department": req.department_id,
                    "price": req.price,
                    "avans": True,
                    "comment": req.month
                }
                res = requests.post(url=url, auth=auth, json=js)
                if 'success' in list(res.json().keys()):
                    update.message.reply_html(f"✅So`rov tasdiqlandi, kassaga chiqishingiz mumkin ID: {req.pk}")
                else:
                    update.message.reply_html("🚫Xatolik yuz berdi")
        step.update({"step": 0})
        Data.objects.filter(telegram_id=worker_id).update(data=step)
        reply_markup = avansButton(hasPermBookRoom(user_id))
        if isCashier(user_id):
            reply_markup = cashierButton()
        update.message.reply_text("Bosh sahifa", reply_markup=reply_markup)

    else:  # oddiy ishchilar
        price = int(step['price'])
        money_split = splitMoney(user_id=worker_id, money=price)
        for month, money in money_split:
            if money == 0:
                continue
            req = Request_price.objects.create(price=money, avans=True, month=months[month - 1],
                                               department_id=Workers.objects.get(
                                                   telegram_id=worker_id).department.ids)
            try:
                obj = Total.objects.filter(full_name__telegram_id=worker_id,
                                           year__in=[datetime.now().year - 1, datetime.now().year],
                                           month=months[month - 1]).first()
                req.workers.add(obj)
            except Exception as ex:
                print(ex)
            step.update({"step": 0})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            staff = getWorker(worker_id)
            text = getAvansText(name=staff.full_name, req=req, month=months[month - 1], salary=obj.itog_1, money=money,
                                balance=obj.ostatok_1 + money)
            if staff.boss:
                message = context.bot.send_message(chat_id=staff.boss.telegram_id, text=text, parse_mode="html",
                                                   reply_markup=acceptInlineButton(req.id))
                create_auto_delete_req(message_id=message.message_id, chat_id=staff.boss.telegram_id,
                                       request_id=req.id)  # Auto delete request
                update.message.reply_text(text=f"✅So`rov {staff.boss.full_name}ga yuborildi, ID:  {req.pk}")
            else:
                try:
                    boss = Workers.objects.filter(is_boss=True,
                                                  department=Workers.objects.get(
                                                      telegram_id=worker_id).department).first()
                    accept_button = acceptInlineButton(req.id)
                    if month >= datetime.now().month and (obj.ostatok_1 <= obj.itog_1 * 0.3
                                                          or money >= obj.itog_1 * 0.7):
                        accept_button = acceptInlineButton2(req.id)
                    message = context.bot.send_message(chat_id=boss.telegram_id, text=text, parse_mode="html",
                                                       reply_markup=accept_button)
                    create_auto_delete_req(message_id=message.message_id, chat_id=boss.telegram_id,
                                           request_id=req.id)  # Auto delete request
                    update.message.reply_text(f"✅So`rov bo`lim boshlig`iga yuborildi, ID: {req.id}")
                except Exception as ex:
                    error = f"{obj}\n{ex.__str__()}"
                    sed_error_to_admin(error)
        reply_markup = avansButton(hasPermBookRoom(user_id))
        if isCashier(user_id):
            reply_markup = cashierButton()
        update.message.reply_text("Bosh sahifa", reply_markup=reply_markup)


def report(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    if not isITStaff(user_id):
        for total in getTotalList(user_id)[-3:]:
            text = getReportTotalText(total)
            sleep(0.1)
            context.bot.send_message(chat_id=user_id, text=text, parse_mode="HTML",
                                     reply_markup=homeButton())

        step["step"] = 3
        Data.objects.filter(telegram_id=user_id).update(data=step)
    else:
        text = "Biz boshqa respublika 😂"
        context.bot.send_message(chat_id=user_id, text=text, parse_mode="HTML",
                                 reply_markup=homeButton())


def home(update: Update, context: CallbackContext, menu_button=None):
    user_id = update.message.from_user.id
    if menu_button is None:
        menu_button = avansButton(hasPermBookRoom(user_id))
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


def sed_error_to_admin(error):
    bot.send_message(chat_id=779890968, text=f"Error: {error}")


def send_boss(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    step.update({"step": 5})
    Data.objects.filter(telegram_id=user_id).update(data=step)
    update.message.reply_html("Boshlig`ingizni tanlang",
                              reply_markup=homeButton())


def setEventName(update: Update, context: CallbackContext):
    update.message.reply_html("Tadbir nomini kiriting", reply_markup=homeButton())
    user_id = update.message.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    step.update({"step": 300})
    Data.objects.filter(telegram_id=user_id).update(data=step)


def bookRooms(update: Update, context: CallbackContext):
    event = update.message.text
    rooms = Rooms.objects.filter(is_active=True)
    user_id = update.message.from_user.id
    step = Data.objects.get(telegram_id=user_id).data
    step.update({"step": 301, "event": event})
    Data.objects.filter(telegram_id=user_id).update(data=step)
    update.message.reply_html("Xonani tanlang", reply_markup=roomListInlineButton(rooms))


def roomTimeTables(room):
    return Timetable.objects.filter(room=room, is_active=True, date__gte=date.today()).order_by('date', 'start_time')


def roomTableText(room, date: date):
    text = f"📅{date.strftime('%Y-%m-%d')}\n" \
           f"Xona: <strong>{room.name}</strong>\n" \
           f"<strong>Band qilingan vaqtlar:</strong>\n"
    for item in roomTimeTables(room).filter(date=date):
        text += f"👤{item.user.full_name}\n" \
                f"Tadbir: <strong>{item.event}</strong>\n" \
                f"🕔{item.start_time.strftime('%H:%M')} - {item.end_time.strftime('%H:%M')}\n\n"
    return text


def freeRoomHours(room, date: date):
    time_table = Timetable.objects.filter(room=room, date=date)
    time_table_list = [i for i in range(8, 19)]
    for item in time_table:
        for i in range(item.start_time.hour, item.end_time.hour):
            if i in time_table_list:
                time_table_list.remove(i)
    return time_table_list


def freeRoomEndHours(room, date: date, start_time: int):
    end_time_list = []
    time_table = Timetable.objects.filter(room=room, date=date, start_time__hour__gte=start_time).order_by('start_time')
    stat_hour = time_table.first().start_time.hour if time_table.exists() else 19
    while start_time < stat_hour:
        start_time += 1
        end_time_list.append(start_time)
    return end_time_list


def selectBookTime(user, room, event, date, start_time, end_time):
    Timetable.objects.create(user=user, room=room, event=event, date=date, start_time=start_time, end_time=end_time)
    return 1


def send_message_to_group(context: CallbackContext, text):
    context.bot.send_message(chat_id=GROUP_ID, text=text, parse_mode="HTML")
