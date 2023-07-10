from django_filters.rest_framework import FilterSet, CharFilter, DateFilter, DateRangeFilter

from apps.staff.models import Workers


class WorkerFilter(FilterSet):
    department = CharFilter(method='by_department')
    # start_date = DateFilter(method='by_start_date')
    # end_date = DateFilter(method='by_end_date')

    class Meta:
        model = Workers
        fields = {
            'job': ['exact'],
            'is_boss': ['exact'],
            'in_office': ['exact'],
            'role': ['exact'],
            'is_active': ['exact'],
        }

    def by_department(self, queryset, name, value):
        worker = self.request.user.workers_set.first()
        if worker.role == Workers.Role.SUPER_ADMIN:
            queryset = queryset.filter(department__name=value)
        else:
            queryset = queryset.filter(department__name=worker.department.name)

        return queryset

    def by_start_date(self, queryset, name, value):
        queryset = queryset.filter(timekeeping__date__gte=value)
        return queryset

    def by_end_date(self, queryset, name, value):
        queryset = queryset.filter(timekeeping__date__lte=value)
        return queryset
