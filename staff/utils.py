import datetime
import threading

from staff.models import Total, getMonthList, Workers, InfTech
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from telegram import Bot
from config.settings import S_TOKEN

bot = Bot(token=S_TOKEN)


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
    next_month = date.today() + relativedelta(months=+1)
    months = getMonthList()
    total_all = Total.objects.filter(full_name__telegram_id=user_id, year=date.today().year,
                                     month=months[date.today().month - 1]).first()
    if total_all.ostatok_1.__ge__(money):
        return (date.today().month, money), (0, 0)
    if total_all.ostatok_1.__eq__(0):
        return (next_month.month, abs(money - total_all.ostatok_1)), (0, 0)
    return (date.today().month, total_all.ostatok_1), (next_month.month, abs(money - total_all.ostatok_1))


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
