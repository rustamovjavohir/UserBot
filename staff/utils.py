import threading

from staff.models import Total, getMonthList, Workers, InfTech, Request_price
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from telegram import Bot
from config.settings import S_TOKEN

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
    total = Total.objects.filter(full_name__telegram_id=user_id)
    for item in total:
        sum_money += item.ostatok_1
    if sum_money.__ge__(money):
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
    total_all = Total.objects.filter(full_name__telegram_id=user_id).first()
    current_day = datetime(int(total_all.year), int(total_all.month_index), 1)
    next_month = nextMonth(total_all)
    if total_all.ostatok_1.__ge__(money):
        return (total_all.month_index, money), (0, 0)
    if total_all.ostatok_1.__eq__(0):
        return (next_month.month, abs(money - total_all.ostatok_1)), (0, 0)
    return (current_day.month, total_all.ostatok_1), (next_month.month, abs(money - total_all.ostatok_1))


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
