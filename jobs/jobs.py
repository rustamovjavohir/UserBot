import requests
from datetime import date
from staff.models import *
from django.db.models import Sum


def updateTotal():
    # months = getMonthList()
    # salary = Salarys.objects.all()
    bonus = Bonus.objects.filter(is_deleted=False)
    leave = Leave.objects.all()

    totals = Total.objects.all().order_by('-id')[:100]
    for total in totals:
        total_bonus = bonus.filter(full_name=total.full_name, year=total.year, month=total.month). \
            aggregate(Sum("bonus")).get('bonus__sum', 0)
        total_paid = bonus.filter(full_name=total.full_name, year=total.year, month=total.month). \
            aggregate(Sum("paid")).get('paid__sum', 0)
        total_fine = leave.filter(full_name=total.full_name, year=total.year, month=total.month). \
            aggregate(Sum("fine")).get('fine__sum', 0)
        if total_bonus is None:
            total_bonus = 0
        if total_paid is None:
            total_paid = 0
        if total_fine is None:
            total_fine = 0
        total.bonuss_2 = total_bonus
        total.paid_2 = total_paid
        total.vplacheno_2 = total_fine
        total.save()


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

# def time(lists: tuple, index: int):
#     lists1 = list(lists)
#     lists1[index] = lists[index].strftime("%d.%m.%Y %H:%M:%S")
#     return tuple(lists1)


# def export_excel():
#     wb = Workbook()
#     wb1 = wb.active
#     wb1.title = "Department"
#     Dep = [obj.name for obj in Department._meta.fields]
#     users_data = Department.objects.all().values_list()
#     for i_col, header in enumerate(Dep, start=1):
#         wb1.cell(row=1, column=i_col, value=header)
#     for i_row, user_data in enumerate(users_data, start=2):
#         for i_col, value in enumerate(user_data, start=1):
#             wb1.cell(row=i_row, column=i_col, value=value)
#
#     wb1 = wb.create_sheet("Workers")
#     Dep = [obj.name for obj in Workers._meta.fields]
#     users_data = Workers.objects.all().values_list()
#     for i_col, header in enumerate(Dep, start=1):
#         wb1.cell(row=1, column=i_col, value=header)
#     for i_row, user_data in enumerate(users_data, start=2):
#         for i_col, value in enumerate(user_data, start=1):
#             wb1.cell(row=i_row, column=i_col, value=value)
#
#     wb1 = wb.create_sheet("Bonus")
#     Dep = [obj.name for obj in Bonus._meta.fields]
#     users_data = Bonus.objects.all().values_list()
#     for i_col, header in enumerate(Dep, start=1):
#         wb1.cell(row=1, column=i_col, value=header)
#     for i_row, user_data in enumerate(users_data, start=2):
#         for i_col, value in enumerate(user_data, start=1):
#             wb1.cell(row=i_row, column=i_col, value=value)
#
#     wb1 = wb.create_sheet("Leave")
#     Dep = [obj.name for obj in Leave._meta.fields]
#     users_data = Leave.objects.all().values_list()
#     for i_col, header in enumerate(Dep, start=1):
#         wb1.cell(row=1, column=i_col, value=header)
#     for i_row, user_data in enumerate(users_data, start=2):
#         user_data = time(user_data, 2)
#         for i_col, value in enumerate(user_data, start=1):
#             wb1.cell(row=i_row, column=i_col, value=value)
#
#     wb1 = wb.create_sheet("Total")
#     Dep = [obj.name for obj in Total._meta.fields]
#     users_data = Total.objects.all().values_list()
#     for i_col, header in enumerate(Dep, start=1):
#         wb1.cell(row=1, column=i_col, value=header)
#     for i_row, user_data in enumerate(users_data, start=2):
#         for i_col, value in enumerate(user_data, start=1):
#             wb1.cell(row=i_row, column=i_col, value=value)
#     file_name = "Database_" + datetime.datetime.now().strftime("%d-%m-%Y") + ".xlsx"
#     wb.save(file_name)
#     oylik_bot.send_document(chat_id=-1001880851912, document=open(file_name, "rb"))
#     os.remove(path=os.path.join(settings.BASE_DIR, file_name))
