from django.contrib import admin
from apps.checking.models import AllowedIPS


# Register your models here.
@admin.register(AllowedIPS)
class AdminAllowedIPS(admin.ModelAdmin):
    list_display = ('name', 'ip')
    search_fields = ('name', 'ip')
    ordering = ('name',)


