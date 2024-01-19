from django.db.models import TextChoices


class TaskStatusChoices(TextChoices):
    NEW = 'new', '🆕Новый'
    IN_PROGRESS = 'in_progress', '🕐В процессе'
    CANCELED = 'canceled', '❌Отменен'
    DONE = 'done', '✅Выполнено'
