from datetime import datetime

from apps.tasks.models import Tasks


def remain_task_text(task: Tasks):
    deadline = task.deadline.astimezone(datetime.now().astimezone().tzinfo)
    text = f"⚠️Deadline\n" \
           f"Vazifa raqami: <strong>№{task.pk}</strong>\n" \
           f"Nomi: <strong>{task.name}</strong>\n" \
           f"Deadline: <strong>{deadline.strftime('%d.%m.%Y %H:%M')}</strong>\n" \
           f"Ma'sul shaxs: <strong>{task.user.full_name}</strong>\n" \
           f"Yaratuvchi: <strong>{task.created_by.full_name}</strong>\n" \
           f"Status: <strong>{task.get_status_display()}</strong>\n"
    return text
