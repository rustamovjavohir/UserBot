from django.db import models


# Create your models here.

class User(models.Model):
    user_telegram_id = models.BigIntegerField(verbose_name="Telegram id")
    username = models.CharField(max_length=120, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    class Status:
        NOT_ANSWERED = "не отвечено"
        COMPLETED = "Завершенный"

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=150, default=Status.NOT_ANSWERED)
    image = models.ImageField(upload_to='message', null=True, blank=True)
    voice = models.CharField(max_length=250, null=True, blank=True)
    message_id = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.user} {self.message}"


class Group(models.Model):
    group_id = models.BigIntegerField(null=True)
