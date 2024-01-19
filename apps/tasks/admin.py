from django.contrib import admin
from apps.tasks.models import Tasks


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'user', 'created_by', 'accepting_date', 'completion_date',
                    'deadline', 'is_active', 'created_at')
    list_filter = ('status', 'user', 'is_active')
    search_fields = ('name', 'description', 'user__full_name')
