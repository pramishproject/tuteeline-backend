import django_filters

from apps.institute_course.models import InstituteApply


class InstituteFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="course_related__course__name")
    min_rating = django_filters.NumberFilter(field_name="rating",lookup_expr="gte")
    max_rating = django_filters.NumberFilter(field_name="rating",lookup_expr="lte")
    eligibility = django_filters.CharFilter(field_name="course_related__eligibility")
    max_fee_range = django_filters.NumberFilter(field_name="course_related__total_fee",lookup_expr='lte')
    min_fee_range = django_filters.NumberFilter(field_name="course_related__total_fee",lookup_expr="gte")
    faculty = django_filters.UUIDFilter(field_name="course_related__faculty")
    class Meta:
        model = InstituteApply
        fields = ['course', 'min_rating','min_rating','country', 'city','eligibility','type','faculty']