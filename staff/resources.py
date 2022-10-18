from django.utils.timezone import localtime
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateTimeWidget, ForeignKeyWidget, DateWidget
from config import settings
from .models import *


class TzDateTimeWidget(DateTimeWidget):

    def render(self, value, obj=None):
        if settings.USE_TZ:
            value = localtime(value)
        return super(TzDateTimeWidget, self).render(value)


class SalarysResource(resources.ModelResource):
    id = Field(attribute="id")
    # full_name = Field(attribute="full_name", column_name="Имя", widget=ForeignKeyWidget(Workers, "full_name"))
    full_name = Field(attribute="full_name", column_name="Имя", widget=ForeignKeyWidget(Workers, "id"))
    # department = Field(attribute="department", column_name="Подразделение")
    year = Field(attribute="year", column_name="Год")
    month = Field(attribute="month", column_name="Месяц")
    salary = Field(attribute="salary", column_name="Оклад")

    class Meta:
        model = Salarys
        skip_unchanged = True
        report_skipped = True
        # exclude = ('id',)
        import_id_fields = ('id', 'full_name', 'year', 'month', 'salary')


class PaidResource(resources.ModelResource):
    id = Field(attribute='id')
    full_name = Field(attribute="full_name", widget=ForeignKeyWidget(Workers, "id"))
    department = Field(attribute="department", column_name="Подразделение")
    month = Field(attribute="month", )
    year = Field(attribute="year", )
    bonus = Field(attribute="bonus", )
    paid = Field(attribute="paid", )

    class Meta:
        model = Bonus
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('id', 'full_name', 'year', 'month', 'bonus', 'paid')


class WorkerResource(resources.ModelResource):
    id = Field(attribute='id')
    full_name = Field(attribute="full_name", column_name="Имя")
    department = Field(attribute="department", column_name="", widget=ForeignKeyWidget(Department, 'id'))
    job = Field(attribute="job", column_name="")
    is_boss = Field(attribute="is_boss", column_name="")
    phone = Field(attribute="phone", column_name="")
    active = Field(attribute="active", column_name="")
    telegram_id = Field(attribute="telegram_id", column_name="")

    # -----------------Server----------------
    # year = Field(column_name="Год")
    # month = Field(column_name="Месяц")
    # salary = Field(column_name="Оклад")
    # bonus = Field(column_name="Бонус")
    # paid = Field(column_name="Штраф")
    # ----------------------------------------

    class Meta:
        model = Workers
        import_id_fields = ('id', 'full_name', 'department', 'job', 'is_boss', 'phone', 'active', 'telegram_id')
        fields = '__all__'
        # exclude = ('id', 'department', 'job', 'phone', 'telegram_id', "is_boss", "active")


class DepartmentResource(resources.ModelResource):
    id = Field(attribute='id')
    name = Field(attribute='name', column_name="Подразделение")
    ids = Field(attribute='ids', column_name="ID")

    class Meta:
        model = Department
        # fields = exclude = ('id',)
        import_id_fields = ("id", 'name', 'ids')


class LeaveResource(resources.ModelResource):
    id = Field(attribute='id')
    full_name = Field(attribute="full_name", widget=ForeignKeyWidget(Workers))
    datetime_create = Field(attribute='datetime_create', widget=DateTimeWidget('%d.%m.%Y %H:%M:%S'))
    month = Field(attribute='month', )
    year = Field(attribute='year')
    fine = Field(attribute='fine')

    class Meta:
        model = Leave
        import_id_fields = ("id", 'full_name', 'month', 'year', 'fine')
