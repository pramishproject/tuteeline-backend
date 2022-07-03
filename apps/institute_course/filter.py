import django_filters

from apps.institute_course.models import InstituteApply


class ApplicationFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="action_field__action")
    # course = django_filters.CharFilter(field_name="course")
    # min_rating = django_filters.NumberFilter(field_name="rating",lookup_expr="gte")
    # max_rating = django_filters.NumberFilter(field_name="rating",lookup_expr="lte")
    # eligibility = django_filters.CharFilter(field_name="course_related__eligibility")
    # max_fee_range = django_filters.NumberFilter(field_name="course_related__total_fee",lookup_expr='lte')
    # min_fee_range = django_filters.NumberFilter(field_name="course_related__total_fee",lookup_expr="gte")
    # faculty = django_filters.UUIDFilter(field_name="course_related__faculty")
    class Meta:
        model = InstituteApply
        fields = ["status","course"]

class ApplicationAggregateFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name="created_at", lookup_expr=('gt'))
    max_date = django_filters.DateFilter(field_name="created_at", lookup_expr=('lt'))
    class Meta:
        model = InstituteApply
        fields = ["min_date", "max_date"]