from django.contrib import admin
from apps.rooms.models import Rooms, Timetable


@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name']

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'start_time', 'end_time', 'date', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'user', 'room']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['user__full_name', 'room__name']

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
