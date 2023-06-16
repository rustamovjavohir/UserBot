from datetime import datetime, date as datetime_date, timedelta
from django.utils.timezone import is_aware, make_naive
import calendar
import openpyxl
from django.http import HttpResponse
from openpyxl.styles import Font, Alignment, NamedStyle, numbers, DEFAULT_FONT


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


def workers_2_xlsx(query, start_date=None, end_date=None):
    month_style = NamedStyle(name='month_style', number_format='mmmm', font=Font(name='Calibri', size=11, bold=True))
    time_style = NamedStyle(name='time_style', number_format='h:mm')
    date_style = NamedStyle(name='date_style', number_format='mm/dd/yyyy')
    start_time_style = NamedStyle(name='start_time_style', number_format='h:mm', font=Font(bold=True))
    today = datetime.now()
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else datetime_date(today.year, today.month, 1)
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime_date(today.year, today.month, 30)
    start_date = datetime_date(start_date.year, start_date.month, start_date.day)
    end_date = datetime_date(end_date.year, end_date.month, end_date.day)
    delta = end_date - start_date
    BODY_ROW = 3
    workbook = openpyxl.load_workbook(filename='media/check_in_out.xlsx')
    worksheet = workbook.active
    month_cell = worksheet.cell(row=1, column=1, value=start_date)
    month_cell.style = month_style
    month_cell.alignment = Alignment(horizontal='center', vertical='center')
    month_cell.number_format = numbers.FORMAT_DATE_TIME6
    worksheet.cell(row=1, column=2).style = start_time_style
    worksheet.cell(row=1, column=3).style = start_time_style
    for enum, data in enumerate(query, start=1):
        worksheet.cell(row=BODY_ROW, column=1, value=enum)
        worksheet.cell(row=BODY_ROW, column=2, value=data.department.name)
        worksheet.cell(row=BODY_ROW, column=3, value=data.full_name)
        for i in range(4, 2 * delta.days + 5):
            time_keeping_date = data.timekeeping_set.filter(date=timedelta(days=(i - 4) / 2) + start_date).first()
            if time_keeping_date:
                if i % 2 == 0:
                    time_keeping_check_in = timedelta(hours=5) + time_keeping_date.check_in.replace(tzinfo=None)
                    check_in_cell = worksheet.cell(row=BODY_ROW, column=i, value=time_keeping_check_in)
                    check_in_cell.number_format = numbers.FORMAT_DATE_TIME6
                    check_in_cell.style = time_style
                    check_in_cell.alignment = Alignment(horizontal='center', vertical='center')
                else:
                    time_keeping_check_out = timedelta(hours=5) + time_keeping_date.check_out.replace(tzinfo=None)
                    check_out_cell = worksheet.cell(row=BODY_ROW, column=i,
                                                    value=time_keeping_check_out)
                    check_out_cell.number_format = numbers.FORMAT_DATE_TIME6
                    check_out_cell.style = time_style
                    check_out_cell.alignment = Alignment(horizontal='center', vertical='center')
            if i % 2 == 0:
                date_cell = worksheet.cell(row=2, column=i, value=timedelta(days=(i - 4) / 2) + start_date)
                date_cell.style = date_style
                date_cell.alignment = Alignment(horizontal='center', vertical='center')
        BODY_ROW += 1

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Workers-timekeeping.xlsx'
    workbook.save(response)
    return response
#
# for i in range(4, 2 * delta.days + 5):
#            time_keeping_date = data.timekeeping_set.filter(date=timedelta(days=(i - 4) / 2) + start_date).first()
#            if time_keeping_date:
#                if i % 2 == 0:
#                    check_in_cell = worksheet.cell(row=BODY_ROW, column=i, value=make_naive(time_keeping_date.check_in))
#                    check_in_cell.number_format = numbers.FORMAT_DATE_TIME6
#                    check_in_cell.style = time_style
#                    check_in_cell.alignment = Alignment(horizontal='center', vertical='center')
#                else:
#                    check_out_cell = worksheet.cell(row=BODY_ROW, column=i,
#                                                    value=make_naive(time_keeping_date.check_out))
#                    check_out_cell.number_format = numbers.FORMAT_DATE_TIME6
#                    check_out_cell.style = time_style
#                    check_out_cell.alignment = Alignment(horizontal='center', vertical='center')
#
#            if i % 2 == 0:
#                date_cell = worksheet.cell(row=2, column=i, value=timedelta(days=(i - 4) / 2) + start_date)
#                date_cell.style = date_style
#                date_cell.alignment = Alignment(horizontal='center', vertical='center')
#        BODY_ROW += 1
