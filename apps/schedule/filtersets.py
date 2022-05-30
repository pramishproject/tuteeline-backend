from django_filters import rest_framework as filters, BaseInFilter, DateFilter

from apps.schedule.models import CounsellingSchedule


class CounselorScheduleSearchFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(
        field_name='date',
        label='date',
    )
    counselor = filters.CharFilter(
        field_name='counselor__user__email'
    )

    class Meta:
        model = CounsellingSchedule
        fields = (
            'date',
            'status',
        )
