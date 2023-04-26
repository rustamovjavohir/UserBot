import requests
from datetime import date, datetime as date_time

from telegram import Bot

from apps.staff.models import Bonus, Leave, Salarys, Total, getMonthList, Workers, Department, Request_price
from config.settings import S_TOKEN
from django.db.models import Sum

bot = Bot(token=S_TOKEN)


def updateTotal():
    try:
        bonus = Bonus.objects.filter(is_deleted=False)
        leave = Leave.objects.all()
        salary_obj = Salarys.objects.all()
        totals = Total.objects.all().order_by('-id')
        for total in totals:
            total_bonus = bonus.filter(full_name=total.full_name, year=total.year, month=total.month). \
                aggregate(Sum("bonus")).get('bonus__sum', 0)
            total_paid = bonus.filter(full_name=total.full_name, year=total.year, month=total.month). \
                aggregate(Sum("paid")).get('paid__sum', 0)
            total_fine = leave.filter(full_name=total.full_name, year=total.year, month=total.month). \
                aggregate(Sum("fine")).get('fine__sum', 0)
            total_salary = salary_obj.filter(full_name=total.full_name, year=total.year, month=total.month). \
                aggregate(Sum("salary")).get('salary__sum', 0)
            if total_bonus is None:
                total_bonus = 0
            if total_paid is None:
                total_paid = 0
            if total_fine is None:
                total_fine = 0
            if total_salary is None:
                total_salary = 0
            total.bonuss_1 = total_bonus
            total.paid_1 = total_paid
            total.vplacheno_1 = total_fine
            total.oklad_1 = total_salary
            total.save()
    except Exception as ex:
        bot.send_message(chat_id=779890968, text=ex.__str__())


def salary():
    months = getMonthList()
    a = date.today().month
    for i in Workers.objects.filter(active=True):
        if Total.objects.filter(full_name=i, month=months[a - 1], year=date.today().year).exists():
            pass
        else:
            Total.objects.create(full_name=i, month=months[a - 1], year=date.today().year)


def auto_request_salary():
    months = getMonthList()
    month = months[int(date.today().month) - 2]
    if int(date.today().month) == 1:
        year = int(date.today().year) - 1
    else:
        year = int(date.today().year)
    dep = Department.objects.all()
    workers = Total.objects.filter(year=str(year), month=month, active=True)
    for i in dep:
        price = 0
        req = Request_price.objects.create(department_id=i.ids, price=0, avans=False)
        for w in workers:
            if i.name == w.department and int(w.ostatok.replace(",", "")) > 0:
                req.workers.add(w)
                price += int(w.ostatok.replace(",", ""))
        Request_price.objects.filter(pk=req.pk).update(price=price)
        if Request_price.objects.get(pk=req.pk).workers.all().exists():
            url = "http://45.142.36.22:4812/ut3/hs/create_applications"
            auth = ("django_admin", "DJango_96547456")
            js = {
                "id": str(req.pk),
                "department": i.ids,
                "price": price,
                "avans": False,
                "comment": ""
            }
            requests.post(url=url, auth=auth, json=js)
        else:
            Request_price.objects.get(pk=req.pk).delete()


def notificationSalary():
    year = date_time.now().year
    months = getMonthList()
    month = months[int(date.today().month)]
    boss = Workers.objects.filter(is_boss=True)
    for bos in boss:
        if not (bos.salarys_set.last().month == month and bos.salarys_set.last().year == str(year)):
            text = f"Ҳурматли <strong>{bos.full_name}</strong>\n" \
                   f"<strong>{month}</strong> ойи учун <strong>{bos.department.name}</strong> " \
                   f"бўлимидаги ҳодимларга ойлик маош ёзишингизни эслатиб қўймоқчимиз"
            try:
                bot.send_message(chat_id=bos.telegram_id, text=text, parse_mode="HTML")
            except Exception as ex:
                bot.send_message(chat_id=779890968, text=ex.__str__(), parse_mode="HTML")


def addSalary():
    year = date_time.now().year
    months = getMonthList()
    month = months[int(date.today().month) - 1]
    next_month = months[int(date.today().month)]
    w_salary = Salarys.objects.filter(year=str(year), month=month)
    # print(w_salary)
    for item in w_salary:
        if not Salarys.objects.filter(full_name=item.full_name, year=str(year), month=next_month).exists():
            Salarys.objects.update_or_create(full_name=item.full_name, salary=item.salary,
                                             year=str(year), month=next_month)

    return year, month, next_month
