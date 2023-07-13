from django.db import models
from apps.staff.models import Workers
from datetime import datetime, timedelta
from pytz import timezone

from config.settings import WORKING_TIME


# Create your models here.

class AllowedIPS(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    ip = models.CharField(max_length=15, verbose_name='IP-адрес')

    def __str__(self):
        return self.ip

    @classmethod
    def checkingIP(cls, ip):
        # Check whether the product is in the table or not
        return ip in cls.objects.values_list('ip', flat=True)

    @classmethod
    def getIPsList(cls):
        return cls.objects.values_list('ip', flat=True)

    class Meta:
        verbose_name = 'Разрешенный IP-адрес'
        verbose_name_plural = 'Разрешенные IP-адреса'


class Timekeeping(models.Model):
    class ActionChoices(models.TextChoices):
        CHECK_IN = 'check_in', 'Приход'
        CHECK_OUT = 'check_out', 'Уход'

    worker = models.ForeignKey(Workers, on_delete=models.DO_NOTHING, verbose_name='Сотрудник')
    check_in = models.DateTimeField(null=True, blank=True, verbose_name='Время прихода')
    check_out = models.DateTimeField(null=True, blank=True, verbose_name='Время ухода')
    date = models.DateField(null=True, blank=True, verbose_name='Дата')
    comment = models.CharField(max_length=300, null=True, blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_deleted = models.BooleanField(default=False, verbose_name='Удален')

    def __str__(self):
        return self.worker.full_name

    @staticmethod
    def get_tz_info():
        return timezone('Asia/Tashkent')

    def setCheckIn(self):
        if not self.check_in:
            self.check_in = datetime.now(tz=self.get_tz_info())
            self.worker.is_active = True
            self.worker.save()
            self.save()

    def setCheckOut(self):
        if datetime.now(tz=self.get_tz_info()) - self.check_in > timedelta(hours=WORKING_TIME):
            self.setCheckOutByApi()

    def setCheckOutByApi(self):
        if not self.check_out and self.check_in:
            self.check_out = datetime.now(tz=self.get_tz_info())
            self.worker.is_active = False
            self.worker.save()
            self.save()

    def setCheckInOrOut(self):
        if self.check_in:
            self.setCheckOut()
        else:
            self.setCheckIn()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def work_time(self):
        if self.check_in and self.check_out:
            return self.check_out - self.check_in
        else:
            return None

    class Meta:
        verbose_name = 'Проверка'
        verbose_name_plural = 'Проверки'
        ordering = ['-date']
