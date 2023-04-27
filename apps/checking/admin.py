from django.contrib import admin
from apps.checking.models import AllowedIPS, Timekeeping


# Register your models here.
@admin.register(AllowedIPS)
class AdminAllowedIPS(admin.ModelAdmin):
    list_display = ('name', 'ip')
    search_fields = ('name', 'ip')
    ordering = ('name',)


@admin.register(Timekeeping)
class AdminTimekeeping(admin.ModelAdmin):
    list_display = ['worker', 'worker_department', 'date', 'check_in', 'check_out', 'created_at']
    list_filter = ['worker', 'date', 'worker__department']
    ordering = ('-date', 'worker__department')

    def worker_department(self, obj):
        return obj.worker.department

    worker_department.short_description = 'Отдел'
