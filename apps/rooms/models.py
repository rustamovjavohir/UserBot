from django.db import models

from apps.staff.models import Workers


# Create your models here.

class Rooms(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return self.name


class Timetable(models.Model):
    user = models.ForeignKey(Workers, on_delete=models.CASCADE, related_name='timetable')
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='timetable')
    event = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        return self.start_time.strftime("%H:%M") + " - " + self.end_time.strftime("%H:%M")
