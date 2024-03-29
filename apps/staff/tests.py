import random

from apps.staff.models import *
from apps.staff.utils import getMonthList


def addBonus(year=2023, month=0):
    months = getMonthList()
    workers = Workers.objects.all()
    for worker in workers:
        Bonus.objects.create(full_name=worker, year=year, month=months[month],
                             bonus=random.randint(99999, 999999) // 100 * 100,
                             paid=random.randint(9999, 99999) // 100 * 100)


def addSalary(year=2023, month=0):
    months = getMonthList()
    workers = Workers.objects.all()
    for worker in workers:
        Salarys.objects.create(full_name=worker, year=year, month=months[month],
                               salary=random.randint(999999, 9999999) // 100 * 100)


def addLeave(year=2023, month=0):
    months = getMonthList()
    workers = Workers.objects.all()
    for worker in workers:
        Leave.objects.create(full_name=worker, year=year, month=months[month],
                             fine=random.randint(99999, 999999) // 1000 * 1000)


def sortedByMonthIndex(iterable, reverse=True):
    return sorted(iterable, key=lambda t: (t.year, t.month_index), reverse=reverse)
