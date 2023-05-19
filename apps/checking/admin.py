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
    readonly_fields = ('created_at', 'check_in', 'check_out', 'date', 'is_deleted')
    date_hierarchy = 'date'

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return self.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_deleted=False)

    def worker_department(self, obj):
        return obj.worker.department

    worker_department.short_description = 'Отдел'
