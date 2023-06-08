from datetime import datetime, date as datetime_date, timedelta
import calendar
import openpyxl
from django.http import HttpResponse
from openpyxl.styles import Font, Alignment, NamedStyle



def workers_2_xlsx2(query):
    HEADER_ROW = 1
    BODY_ROW = 2
    today = datetime.now()
    date = today.strftime("%Y-%m-%d")
    openpyxl.load_workbook(filename='media/check_in_out.xlsx')
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    bold_font = Font(bold=True)
    alignment = Alignment(horizontal='center', vertical='center')

    pk = query.model._meta.get_field('id')
    full_name = query.model._meta.get_field('full_name')
    department = query.model._meta.get_field('department')
    job = query.model._meta.get_field('job')
    role = query.model._meta.get_field('role')
    phone = query.model._meta.get_field('phone')

    worksheet.cell(row=HEADER_ROW, column=1, value=pk.verbose_name).font = bold_font
    worksheet.cell(row=HEADER_ROW, column=2, value=department.verbose_name).font = bold_font
    worksheet.cell(row=HEADER_ROW, column=3, value=full_name.verbose_name).font = bold_font
    worksheet.cell(row=HEADER_ROW, column=4, value=job.verbose_name).font = bold_font
    worksheet.cell(row=HEADER_ROW, column=5, value=role.verbose_name).style = bold_font, alignment

    for enum, data in enumerate(query, start=1):
        worksheet.cell(row=BODY_ROW, column=1, value=enum).alignment = alignment
        worksheet.cell(row=BODY_ROW, column=2, value=data.department.name).alignment = alignment
        worksheet.cell(row=BODY_ROW, column=3, value=data.full_name).alignment = alignment
        worksheet.cell(row=BODY_ROW, column=4, value=data.job).alignment = alignment
        BODY_ROW += 1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Workers-{date}.xlsx'
    workbook.save(response)
    return response


def workers_2_xlsx(query):
    time_style = NamedStyle(name='time_style', number_format='h:mm')
    HEADER_ROW = 3
    BODY_ROW = 3
    today = datetime.now()
    date = today.strftime("%Y-%m-%d")
    workbook = openpyxl.load_workbook(filename='media/check_in_out.xlsx')
    worksheet = workbook.active
    _now = datetime.now()
    for enum, data in enumerate(query, start=1):
        worksheet.cell(row=BODY_ROW, column=1, value=enum)
        worksheet.cell(row=BODY_ROW, column=2, value=data.department.name)
        worksheet.cell(row=BODY_ROW, column=3, value=data.full_name)
        # worksheet.cell(row=BODY_ROW, column=3, value=_now.strftime("%H:%M"))
        worksheet.cell(row=BODY_ROW, column=4, value=timedelta(seconds=60000))
        BODY_ROW += 1

    # workbook.iter_rows(min_row=HEADER_ROW, max_row=BODY_ROW, min_col=1, max_col=3)
    # set_timekeeping_2_workbook(worksheet, query, BODY_ROW)

    worksheet.cell(row=3, column=7, value="salom")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Workers-{date}.xlsx'
    workbook.save(response)
    return response


def set_timekeeping_2_workbook(worksheet, query, BODY_ROW: int = 3):
    _now = datetime.now()
    range_date = calendar.monthrange(_now.year, _now.month)[1]
    start_date = date(_now.year, _now.month, 1)
    for day in range(range_date):
        _date = start_date + timedelta(days=day)
        worksheet.cell(row=3, column=4, value=start_date)

    # for data in query:
    #     for timekeeping in data.timekeeping_set.all():
    #         for day in range(1, calendar.monthrange(timekeeping.date.year, timekeeping.date.month)[1] + 1):
    #             worksheet.cell(row=BODY_ROW, column=1, value=timekeeping.worker.department.name)
    #             worksheet.cell(row=BODY_ROW, column=2, value=timekeeping.worker.full_name)
    #             worksheet.cell(row=BODY_ROW, column=3, value=timekeeping.date)
    #             worksheet.cell(row=BODY_ROW, column=4, value=timekeeping.check_in)
    #             worksheet.cell(row=BODY_ROW, column=5, value=timekeeping.check_out)
    #             BODY_ROW += 1
    #         worksheet.cell(row=BODY_ROW, column=4, value=timekeeping.check_in)
    #         worksheet.cell(row=BODY_ROW, column=5, value=timekeeping.check_out)
    #         BODY_ROW += 1
    return worksheet


def timekeeping_2_xlsx(query):
    HEADER_ROW = 3
    BODY_ROW = 2
    today = datetime.now()
    date = today.strftime("%Y-%m-%d")
    workbook = openpyxl.load_workbook(filename='media/check_in_out.xlsx')
    worksheet = workbook.active

    for enum, data in enumerate(query, start=1):
        worksheet.cell(row=BODY_ROW, column=1, value=enum)
        worksheet.cell(row=BODY_ROW, column=2, value=data.worker.department.name)
        worksheet.cell(row=BODY_ROW, column=3, value=data.worker.full_name)

        BODY_ROW += 1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Workers-{date}.xlsx'
    workbook.save(response)
    return response
