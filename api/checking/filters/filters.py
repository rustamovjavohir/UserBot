from django_filters.rest_framework import FilterSet, CharFilter, DateFilter, DateRangeFilter

from apps.checking.models import Timekeeping


class TimekeepingFilter(FilterSet):
    date_range = DateRangeFilter(field_name='date')
    department = CharFilter(method='by_department')

    class Meta:
        model = Timekeeping
        fields = ('date', 'department')

    def by_department(self, queryset, name, value):
        queryset = queryset.filter(worker__department__name=value)
        return queryset
