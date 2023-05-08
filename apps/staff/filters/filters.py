from django.contrib.admin import SimpleListFilter
from apps.staff.models import Department


class DepartmentFilter(SimpleListFilter):
    title = 'Подразделение'
    parameter_name = 'department_id'
    model = Department

    def get_department_query(self):
        return self.model.objects.all()

    def get_department_list_by_attr(self, attr, flat=True):
        return self.get_department_query().values_list(attr, flat=flat)

    def get_department_id_name(self):
        return self.get_department_query().values_list('ids', 'name')

    def lookups(self, request, model_admin):
        lookup_list = []
        for department_id, department in self.get_department_id_name():
            lookup_list.append((department_id, department))
        return lookup_list

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(department_id=self.value())
        return queryset
