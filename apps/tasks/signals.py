from apps.staff.utils import send_status_notification, task_completed_notification
from apps.tasks.choices import TaskStatusChoices
from apps.tasks.models import Tasks
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver


@receiver(pre_save, sender=Tasks)
def check_task_status(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(id=instance.id).first()
    if old_instance:
        if old_instance.status != instance.status:
            if instance.status == TaskStatusChoices.DONE:
                task_completed_notification(instance)
            try:
                send_status_notification(instance)
            except Exception as e:
                print(e)
