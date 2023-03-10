from django.utils.timezone import localtime
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateTimeWidget, ForeignKeyWidget, DateWidget
from config import settings
from apps.staff.models import *


class TzDateTimeWidget(DateTimeWidget):

    def render(self, value, obj=None):
        if settings.USE_TZ:
            value = localtime(value)
        return super(TzDateTimeWidget, self).render(value)


class SalarysResource(resources.ModelResource):
    # id = Field(attribute="id", column_name="Номер")
    full_name = Field(attribute="full_name", column_name="Имя", widget=ForeignKeyWidget(Workers, "full_name"))
    # full_name = Field(attribute="full_name", column_name="Имя", widget=ForeignKeyWidget(Workers, "id")) # import
    department = Field(attribute="department", column_name="Подразделение")
    year = Field(attribute="year", column_name="Год")
    month = Field(attribute="month", column_name="Месяц")
    salary = Field(attribute="salary", column_name="Оклад")

    class Meta:
        model = Salarys
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('full_name', 'year', 'month', 'salary')


class PaidResource(resources.ModelResource):
    id = Field(attribute='id', column_name="ID")
    full_name = Field(attribute="full_name", widget=ForeignKeyWidget(Workers, "full_name"))
    department = Field(attribute="department", column_name="Подразделение")
    year = Field(attribute="year", column_name="Год")
    month = Field(attribute="month", column_name="Месяц")
    bonus = Field(attribute="bonus", column_name="Бонус")
    paid = Field(attribute="paid", column_name="Штраф")

    class Meta:
        model = Bonus
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('full_name', 'year', 'month', 'bonus', 'paid')


class WorkerResource(resources.ModelResource):
    # full_name = Field(attribute="full_name", column_name="Имя")
    # year = Field(column_name="Год")
    # month = Field(column_name="Месяц")
    # salary = Field(column_name="Оклад")
    # bonus = Field(column_name="Бонус")
    # paid = Field(column_name="Штраф")

    id = Field(attribute='id')
    full_name = Field(attribute="full_name", column_name="Имя")
    department = Field(attribute="department", column_name="", widget=ForeignKeyWidget(Department, 'name'))
    job = Field(attribute="job", column_name="")
    is_boss = Field(attribute="is_boss", column_name="")
    phone = Field(attribute="phone", column_name="")
    active = Field(attribute="active", column_name="")
    telegram_id = Field(attribute="telegram_id", column_name="")

    class Meta:
        model = Workers
        exclude = ('id', 'department', 'job', 'phone', 'telegram_id', "is_boss", "active")
        # import_id_fields = ('id', 'full_name', 'department', 'job', 'is_boss', 'phone', 'active', 'telegram_id')


class DepartmentResource(resources.ModelResource):
    id = Field(attribute='id')
    name = Field(attribute='name', column_name="Подразделение")
    ids = Field(attribute='ids', column_name="ID")

    class Meta:
        model = Department
        # fields = exclude = ('id',)
        import_id_fields = ('name', 'ids')


class LeaveResource(resources.ModelResource):
    id = Field(attribute='id')
    full_name = Field(attribute="full_name", widget=ForeignKeyWidget(Workers, "full_name"))
    datetime_create = Field(attribute='datetime_create', widget=DateTimeWidget('%d.%m.%Y %H:%M:%S'))
    month = Field(attribute='month', )
    year = Field(attribute='year')
    fine = Field(attribute='fine')

    class Meta:
        model = Leave
        import_id_fields = ('full_name', 'month', 'year', 'fine')


class InfTech(resources.ModelResource):
    full_name = Field(attribute="full_name", column_name="Ф.И.О")
    department = Field(attribute="department", column_name="Подразделение")
    job = Field(attribute="job", column_name="Должность")
    phone = Field(attribute="phone", column_name="Телефон номер")
    active = Field(attribute="active", column_name="Статус")

    class Meta:
        model = InfTech
        import_id_fields = ('full_name', 'department', 'job', 'phone', 'active')
