from django.contrib import admin
from apps.checking.models import AllowedIPS, Timekeeping
import pytz


# Register your models here.
@admin.register(AllowedIPS)
class AdminAllowedIPS(admin.ModelAdmin):
    list_display = ('name', 'ip')
    search_fields = ('name', 'ip')
    ordering = ('name',)


@admin.register(Timekeeping)
class AdminTimekeeping(admin.ModelAdmin):
    list_display = ['worker', 'worker_department', 'date', 'check_in_pretty', 'check_out_pretty']
    list_filter = ['worker', 'date', 'worker__department']
    ordering = ('-date', 'worker__department')
    readonly_fields = ('created_at', 'check_in', 'check_out', 'date', 'is_deleted')
    date_hierarchy = 'date'

    @staticmethod
    def get_tz_info():
        return pytz.timezone('Asia/Tashkent')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return self.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_deleted=False)

    def check_in_pretty(self, obj):
        if obj.check_in:
            return obj.check_in.astimezone(self.get_tz_info()).strftime("%H:%M")
        else:
            return '-'

    check_in_pretty.short_description = 'Время прихода'

    def check_out_pretty(self, obj):
        if obj.check_out:
            return obj.check_out.astimezone(self.get_tz_info()).strftime("%H:%M")
        return '-'

    check_out_pretty.short_description = 'Время ухода'

    def worker_department(self, obj):
        return obj.worker.department

    worker_department.short_description = 'Отдел'
