from django.db import models
from apps.staff.models import Workers

from apps.tasks.choices import TaskStatusChoices


class Tasks(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название задачи')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание задачи')
    status = models.CharField(max_length=255,
                              choices=TaskStatusChoices.choices,
                              default=TaskStatusChoices.NEW,
                              verbose_name='Статус задачи')
    user = models.ForeignKey(Workers,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    accepting_date = models.DateTimeField(null=True, blank=True,
                                          verbose_name='Дата принятия')
    completion_date = models.DateTimeField(null=True, blank=True,
                                           verbose_name='Дата завершения')
    deadline = models.DateTimeField(null=True, blank=True,
                                    verbose_name='Дедлайн')
    created_by = models.ForeignKey(Workers,
                                   on_delete=models.CASCADE,
                                   related_name='created_by',
                                   verbose_name='Создано')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активность')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата изменения')
    data = models.JSONField(default=dict,
                            verbose_name='Данные')

    def __str__(self):
        return f"{self.name[:20]}-{self.user}"

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('-created_at',)

    def send_status_notification(self):
        sender_id = self.created_by.telegram_id
        sender_message_id = self.data.get('sender_message_id', None)
        if sender_message_id:
            sender_message_id = int(sender_message_id)
