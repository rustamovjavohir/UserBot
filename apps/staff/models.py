import datetime

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.safestring import mark_safe
from telegram import Bot

from config.settings import S_TOKEN

bot = Bot(S_TOKEN)


def getMonths() -> list:
    months = [
        ("Январь", "Январь"),
        ("Февраль", "Февраль"),
        ("Март", "Март"),
        ("Апрель", "Апрель"),
        ("Май", "Май"),
        ("Июнь", "Июнь"),
        ("Июль", "Июль"),
        ("Август", "Август"),
        ("Сентябрь", "Сентябрь"),
        ("Октябрь", "Октябрь"),
        ("Ноябрь", "Ноябрь"),
        ("Декабрь", "Декабрь"),
    ]
    return months


def getMonthList() -> list:
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
              "Ноябрь", "Декабрь"]
    return months


class Department(models.Model):
    name = models.CharField(max_length=70, verbose_name="Подразделение")
    ids = models.CharField(max_length=70, default="", verbose_name="ID")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделение"


class InfTech(models.Model):
    full_name = models.CharField(max_length=70, verbose_name="Ф.И.О", unique=True)
    # department = models.CharField(default='АЙТи отдел', max_length=250, verbose_name="Подразделение")
    department = models.ForeignKey(to=Department, on_delete=models.DO_NOTHING, verbose_name="Подразделение")
    job = models.CharField(max_length=70, verbose_name="Должность")
    is_boss = models.BooleanField(default=False, verbose_name="Начальник отдела")
    phone = models.CharField(max_length=70, verbose_name="Телефон номер")
    active = models.BooleanField(default=True, verbose_name="Статус")
    telegram_id = models.BigIntegerField(null=True, blank=True, verbose_name="Telegram ID")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "АЙТишник"
        verbose_name_plural = "АЙТишники"


class ITRequestPrice(models.Model):
    secondId = models.IntegerField(null=True, blank=True, verbose_name="Запрос ИД")
    workers = models.ManyToManyField(InfTech)
    department_id = models.CharField(max_length=70)
    month = models.CharField(choices=getMonths(), max_length=250, null=True, blank=True)
    price = models.BigIntegerField()
    avans = models.BooleanField()
    comment = models.CharField(max_length=2560, default="")
    answer = models.BooleanField(default=False)
    status = models.CharField(max_length=256, default="")

    @property
    def department(self):
        return self.department_id

    department.fget.short_description = "Подразделение"

    @property
    def all_workers(self):
        if self.workers.all().exists():
            string = ""
            for i in self.workers.all():
                string += i.full_name + '<br>'
            return mark_safe(string)
        else:
            return ""

    all_workers.fget.short_description = "Сотрудники"

    class Meta:
        verbose_name = "АЙТи отдел Зарплаты/аванс запрос"
        verbose_name_plural = "АЙТи отдел Зарплаты/aванс запрос"


class Workers(models.Model):
    full_name = models.CharField(max_length=70, verbose_name="Ф.И.О", unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Подразделение")
    job = models.CharField(max_length=70, verbose_name="Должность")
    is_boss = models.BooleanField(default=False, verbose_name="Начальник отдела")
    phone = models.CharField(max_length=70, verbose_name="Телефон номер")
    active = models.BooleanField(default=True, verbose_name="Статус")
    telegram_id = models.BigIntegerField(null=True, blank=True, verbose_name="Telegram ID")
    boss = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Главный")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    is_access = models.BooleanField(default=False, null=True, blank=True, verbose_name="Право доступа")
    in_office = models.BooleanField(default=True, null=True, blank=True, verbose_name="В офисе")
    start_work = models.TimeField(default=datetime.datetime.strptime("09:00:00", '%H:%M:%S').time(),
                                  verbose_name="Начало работы")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"


class Salarys(models.Model):
    full_name = models.ForeignKey(Workers, verbose_name="Ф.И.О", on_delete=models.CASCADE)
    year = models.CharField(default=datetime.datetime.now().year, verbose_name="Год", max_length=10)
    month = models.CharField(choices=getMonths(), verbose_name="Месяц", max_length=100)
    salary = models.IntegerField(verbose_name="Оклад")

    @property
    def musk_salary(self):
        return "{:,}".format(self.salary)

    musk_salary.fget.short_description = "Оклад"

    @property
    def department(self):
        return self.full_name.department.name

    department.fget.short_description = "Подразделение"

    class Meta:
        unique_together = (("full_name", "year", "month"),)
        verbose_name = "Зарплаты"
        verbose_name_plural = "Зарплаты"


class Bonus(models.Model):
    bonus_id = models.CharField(max_length=250, null=True, blank=True, verbose_name="1c bonus ид")
    full_name = models.ForeignKey(Workers, verbose_name="Ф.И.О", on_delete=models.CASCADE)
    month = models.CharField(choices=getMonths(), verbose_name="Месяц", max_length=100)
    year = models.CharField(default=datetime.datetime.now().year, verbose_name="Год", max_length=10)
    bonus = models.IntegerField(default=0, verbose_name="Бонус")
    paid = models.IntegerField(default=0, verbose_name="Штраф")
    is_deleted = models.BooleanField(default=False)

    @property
    def department(self):
        return self.full_name.department.name

    department.fget.short_description = "Подразделение"

    @property
    def musk_bonus(self):
        return "{:,}".format(self.bonus)

    musk_bonus.fget.short_description = "Бонус"

    @property
    def musk_paid(self):
        return "{:,}".format(self.paid)

    musk_paid.fget.short_description = "Штраф"

    def send_bonus_notification(self):
        bot.send_message(self.full_name.telegram_id,
                         f"Вам начислен бонус в размере {self.musk_bonus} сум за {self.month} месяц")

    def send_paid_notification(self):
        bot.send_message(self.full_name.telegram_id,
                         f"Вам начислен штраф в размере {self.musk_paid} сум за {self.month} месяц")

    class Meta:
        verbose_name = "Бонус и шртаф"
        verbose_name_plural = "Бонус и шртаф"


class Leave(models.Model):
    full_name = models.ForeignKey(Workers, verbose_name="Ф.И.О", on_delete=models.CASCADE)
    datetime_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", null=True)
    month = models.CharField(choices=getMonths(), verbose_name="Месяц", max_length=100)
    year = models.CharField(default=datetime.datetime.now().year, verbose_name="Год", max_length=10)
    fine = models.IntegerField(default=0, verbose_name="Выплачено")

    @property
    def musk_fine(self):
        return "{:,}".format(self.fine)

    musk_fine.fget.short_description = "Выплачено"

    @property
    def department(self):
        return self.full_name.department.name

    department.fget.short_description = "Подразделение"

    class Meta:
        verbose_name = "Выплаты"
        verbose_name_plural = "Выплаты"


class Total(models.Model):
    full_name = models.ForeignKey(Workers, verbose_name="Ф.И.О", on_delete=models.CASCADE)
    year = models.CharField(verbose_name="Год", max_length=10)
    month = models.CharField(choices=getMonths(), verbose_name="Месяц", max_length=100)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    oklad_1 = models.IntegerField(default=0, verbose_name="Оклад")
    bonuss_1 = models.IntegerField(default=0, verbose_name="Бонус")
    paid_1 = models.IntegerField(default=0, verbose_name="Штраф")
    vplacheno_1 = models.IntegerField(default=0, verbose_name="Выплачено")

    # queyset
    salary = Salarys.objects.all()
    bonus = Bonus.objects.filter(is_deleted=False)
    leave = Leave.objects.all()

    @property
    def month_index(self):
        months = getMonthList()
        return months.index(self.month) + 1

    @property
    def oklad(self):
        return "{:,}".format(self.oklad_1)

    oklad.fget.short_description = "Оклад"

    @property
    def bonuss(self):
        return "{:,}".format(self.bonuss_1)

    bonuss.fget.short_description = "Бонус"

    @property
    def paid(self):
        return "{:,}".format(self.paid_1)

    paid.fget.short_description = "Штраф"

    @property
    def itog_1(self):
        return int(self.oklad_1) - int(self.paid_1) + int(self.bonuss_1)

    @property
    def itog(self):
        return "{:,}".format(self.itog_1)

    itog.fget.short_description = "Итого"

    @property
    def vplacheno(self):
        return "{:,}".format(self.vplacheno_1)

    vplacheno.fget.short_description = "Выплачено"

    @property
    def waiting_1(self):
        request_price = self.request_price_set.filter(answer=False, month=self.month, avans=True,
                                                      workers__full_name__full_name=self.full_name). \
            aggregate(Sum("price")).get('price__sum', 0)
        if request_price is None:
            request_price = 0
        return request_price

    @property
    def waiting(self):
        return "{:,}".format(self.waiting_1)

    waiting.fget.short_description = "Ожидание"

    @property
    def ostatok_1(self):
        return int(self.itog_1) - int(self.vplacheno_1) - int(self.waiting_1)

    @property
    def ostatok(self):
        return "{:,}".format(self.ostatok_1)

    ostatok.fget.short_description = "Остаток"

    @property
    def department(self):
        return self.full_name.department.name

    department.fget.short_description = "Подразделение"

    def __str__(self):
        return f"{self.full_name.full_name} {self.id}"

    class Meta:
        verbose_name = "Итого"
        verbose_name_plural = "Итого"


class Request_price(models.Model):
    workers = models.ManyToManyField(Total)
    department_id = models.CharField(max_length=70)
    month = models.CharField(choices=getMonths(), max_length=250, null=True, blank=True, verbose_name="Месяц")
    price = models.BigIntegerField(verbose_name="Цена")
    avans = models.BooleanField(verbose_name="Аванс")
    comment = models.CharField(max_length=2560, default="", null=True, blank=True)
    answer = models.BooleanField(default=False, verbose_name="Ответил")
    status = models.CharField(max_length=256, default="", null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    departments = Department.objects.all()

    @property
    def department(self):
        try:
            return self.departments.filter(ids=self.department_id)[0].name
        except:
            return self.department_id

    department.fget.short_description = "Подразделение"

    @property
    def all_workers(self):
        if self.workers.all().exists():
            string = ""
            for i in self.workers.all():
                string += i.full_name.full_name + '<br>'
            return mark_safe(string)
        else:
            return ""

    all_workers.fget.short_description = "Сотрудники"

    class Meta:
        verbose_name = "Зарплаты/аванс запрос"
        verbose_name_plural = "Зарплаты/aванс запрос"


class Data(models.Model):
    telegram_id = models.BigIntegerField()
    data = models.JSONField(default=dict)


class Notification(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    text = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class TotalDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    month = models.CharField(max_length=20, choices=getMonths(), verbose_name="Месяц")
    year = models.CharField(max_length=4, default=datetime.datetime.now().year, verbose_name="Год")

    salary = Salarys.objects.all()
    bonus = Bonus.objects.filter(is_deleted=False)
    leave = Leave.objects.all()

    @property
    def oklad_1(self):
        try:
            salary = self.salary.filter(full_name__department=self.department, month=self.month,
                                        year=self.year).aggregate(Sum('salary')).get("salary__sum")
            if salary is None:
                salary = 0
        except:
            salary = 0
        return salary

    @property
    def oklad(self):
        return "{:,}".format(self.oklad_1)

    oklad.fget.short_description = "Оклад"

    @property
    def bonuss_1(self):
        try:
            bonus = self.bonus.filter(full_name__department=self.department, month=self.month,
                                      year=self.year).aggregate(Sum('bonus')).get("bonus__sum")
            if bonus is None:
                bonus = 0
        except:
            bonus = 0
        return bonus

    @property
    def bonuss(self):
        return "{:,}".format(self.bonuss_1)

    bonuss.fget.short_description = "Бонус"

    @property
    def paid_1(self):
        try:
            paid = self.bonus.filter(full_name__department=self.department, month=self.month,
                                     year=self.year).aggregate(Sum('paid')).get("paid__sum")
            if paid is None:
                paid = 0
        except:
            paid = 0
        return paid

    @property
    def paid(self):
        return "{:,}".format(self.paid_1)

    paid.fget.short_description = "Штраф"

    @property
    def itog_1(self):
        return int(self.oklad_1) - int(self.paid_1) + int(self.bonuss_1)

    @property
    def itog(self):
        return "{:,}".format(self.itog_1)

    itog.fget.short_description = "Итого"

    @property
    def vplacheno_1(self):
        leave = self.leave.filter(full_name__department=self.department, month=self.month,
                                  year=self.year).aggregate(Sum('fine')).get("fine__sum")
        if leave is None:
            leave = 0
        return leave

    @property
    def vplacheno(self):
        return "{:,}".format(self.vplacheno_1)

    vplacheno.fget.short_description = "Выплачено"

    @property
    def ostatok_1(self):
        return int(self.itog_1) - int(self.vplacheno_1)

    @property
    def ostatok(self):
        return "{:,}".format(self.ostatok_1)

    ostatok.fget.short_description = "Остаток"

    class Meta:
        verbose_name = "Итого Подразделение"
        verbose_name_plural = "Итого Подразделение"
