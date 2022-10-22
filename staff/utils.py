import datetime

from staff.models import Total, getMonthList
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


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
