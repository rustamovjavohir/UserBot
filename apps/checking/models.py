from django.db import models


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
