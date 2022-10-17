from django.utils.timezone import localtime
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateTimeWidget, ForeignKeyWidget
from config import settings
from .models import *


class TzDateTimeWidget(DateTimeWidget):

    def render(self, value, obj=None):
        if settings.USE_TZ:
            value = localtime(value)
        return super(TzDateTimeWidget, self).render(value)


class OrderResource(resources.ModelResource):
    # id = Field(attribute="id", column_name="Номер")
    full_name = Field(attribute="full_name", column_name="Имя", widget=ForeignKeyWidget(Workers, "full_name"))
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
    full_name = Field(attribute="full_name", column_name="Имя", widget=ForeignKeyWidget(Workers, "full_name"))
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
    full_name = Field(attribute="full_name", column_name="Имя")
    year = Field(column_name="Год")
    month = Field(column_name="Месяц")
    salary = Field(column_name="Оклад")
    bonus = Field(column_name="Бонус")
    paid = Field(column_name="Штраф")


    class Meta:
        model = Workers
        exclude = ('id', 'department', 'job', 'phone', 'telegram_id', "is_boss", "active")
