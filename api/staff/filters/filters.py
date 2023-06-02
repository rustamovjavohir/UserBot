from django_filters.rest_framework import FilterSet, CharFilter, DateFilter, DateRangeFilter

from apps.staff.models import Workers


class WorkerFilter(FilterSet):
    department = CharFilter(method='by_department')

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
        queryset = queryset.filter(department__name=value)
        return queryset
