from datetime import date

import requests
from django.contrib import admin, messages
from django.db.models import Sum
from django.utils.translation import ngettext
from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin

from config.settings import URL_1C
from .resources import *
from staff.models import *


@admin.register(Workers)
class WorkersAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ["full_name", "department", "job", "phone", "is_boss"]
    list_display_links = ["full_name", "department", "job", "phone"]
    list_filter = ("department",)
    search_fields = ["full_name", "department__name", "job"]
    list_editable = ["is_boss"]
    resource_class = WorkerResource

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


@admin.register(Salarys)
class SalaryAdmin(ImportExportModelAdmin):
    # change_list_template = 'salary/change_list.html'
    change_list_template = 'import_export/change_list_import_export.html'
    list_display = ["full_name", "department", "year", "month", "musk_salary"]
    list_display_links = ["full_name"]
    list_filter = ("full_name__full_name", "full_name__department__name", "year", "month")
    search_fields = ["full_name__full_name", "month"]
    resource_class = SalarysResource

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
            salary = sum([data.salary for data in qs])

            my_context = {
                'salary': "{:,}".format(salary)
            }
            return super(SalaryAdmin, self).changelist_view(request,
                                                            extra_context=my_context)
        except (AttributeError, KeyError):
            return response

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


@admin.register(Bonus)
class BonusAdmin(ImportExportModelAdmin):
    # change_list_template = 'paid/change_list.html'
    change_list_template = 'import_export/change_list_import_export.html'
    list_display = ["full_name", "department", "month", "year", "musk_bonus", "musk_paid"]
    list_display_links = ["full_name"]
    list_filter = ("full_name__full_name", "full_name__department__name", "year", "month")
    search_fields = ["full_name__full_name", "month"]
    resource_class = PaidResource

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
            bonus = sum([data.bonus for data in qs])
            paid = sum([data.paid for data in qs])

            my_context = {
                'bonus': "{:,}".format(bonus),
                'paid': "{:,}".format(paid)
            }
            return super(BonusAdmin, self).changelist_view(request,
                                                           extra_context=my_context)
        except (AttributeError, KeyError):
            return response

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


@admin.register(Leave)
class LeaveAdmin(ImportExportModelAdmin):
    change_list_template = 'import_export/change_list_import_export.html'
    list_display = ["full_name", "datetime_create", "department", "year", "month", "musk_fine"]
    list_display_links = ["full_name"]
    list_filter = ("full_name__full_name", "full_name__department__name", "year", "month")
    search_fields = ["full_name__full_name", "month"]
    resource_class = LeaveResource

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:

            qs = response.context_data['cl'].queryset
            fine = sum([data.fine for data in qs])

            my_context = {
                'fine': "{:,}".format(fine)
            }
            return super(LeaveAdmin, self).changelist_view(request,
                                                           extra_context=my_context)
        except (AttributeError, KeyError):
            return response

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


@admin.register(Request_price)
class DataAdmin(admin.ModelAdmin):
    list_display = ["id", "all_workers", "department", "month", "price", "avans", "answer"]
    list_display_links = ["all_workers"]


@admin.register(Total)
class TotalAdmin(admin.ModelAdmin):
    change_list_template = 'import_export/change_list_import_export.html'
    list_display = ["full_name", "department", "year", "month", "oklad", "bonuss", "paid", "itog", "vplacheno",
                    "ostatok"]
    list_display_links = ["full_name"]
    list_filter = ("full_name__full_name", "full_name__department__name", "year", "month")
    search_fields = ["full_name__full_name", "month"]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
            oklad = sum([data.oklad_1 for data in qs])
            bonus = sum([data.bonuss_1 for data in qs])
            paid = sum([data.paid_1 for data in qs])
            itog = sum([data.itog_1 for data in qs])
            vplacheno = sum([data.vplacheno_1 for data in qs])
            ostatok = sum([data.ostatok_1 for data in qs])
            my_context = {
                'oklad': "{:,}".format(oklad),
                'bonus': "{:,}".format(bonus),
                'paid': "{:,}".format(paid),
                'itog': "{:,}".format(itog),
                'vplacheno': "{:,}".format(vplacheno),
                'ostatok': "{:,}".format(ostatok),
            }
            return super(TotalAdmin, self).changelist_view(request,
                                                           extra_context=my_context)
        except (AttributeError, KeyError):
            return response


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    actions = ["make_published"]
    resource_class = DepartmentResource

    def make_published(self, request, queryset):
        success = ""
        error = ""

        months = getMonthList()

        month = months[int(date.today().month) - 2]
        if int(date.today().month) == 1:
            year = int(date.today().year) - 1
        else:
            year = int(date.today().year)
        dep = queryset
        workers = Total.objects.filter(year=str(year), month=month)
        for i in dep:
            price = 0
            req = Request_price.objects.create(department_id=i.ids, price=0, avans=False)
            for w in workers:
                if i.name == w.department and int(w.ostatok.replace(",", "")) > 0:
                    req.workers.add(w)
                    price += int(w.ostatok.replace(",", ""))
            Request_price.objects.filter(pk=req.pk).update(price=price)
            if Request_price.objects.get(pk=req.pk).workers.all().exists():
                url = f"{URL_1C}ut3/hs/create_applications"
                auth = ("django_admin", "DJango_96547456")
                js = {
                    "id": str(req.pk),
                    "department": i.ids,
                    "price": price,
                    "avans": False,
                    "comment": ""
                }
                res = requests.post(url=url, auth=auth, json=js)
                if 'success' in list(res.json().keys()):
                    success += i.name + ", "
                else:
                    error += i.name + ", "
                    Request_price.objects.get(pk=req.pk).delete()
            else:
                error += i.name + ", "
                Request_price.objects.get(pk=req.pk).delete()
        if len(success) > 0 and len(error) > 0:
            self.message_user(request,
                              message=f"Заявки на зарплату отделам {success}успешно отправлены. Заявки на зарплату в отделы {error}были отправлены безуспешно.",
                              level=messages.SUCCESS)
        elif len(success) > 0:
            self.message_user(request,
                              message=f"Заявки на зарплату отделам {success}успешно отправлены.",
                              level=messages.SUCCESS)
        else:
            self.message_user(request,
                              message=f"Заявки на зарплату в отделы {error}были отправлены безуспешно.",
                              level=messages.ERROR)

    months = getMonthList()

    month = months[int(date.today().month) - 2]
    make_published.short_description = f'Отправить запрос зарплаты для сотрудников за {month} месяц'
