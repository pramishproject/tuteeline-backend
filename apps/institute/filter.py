import django_filters
from django.db.models import Q

from apps.institute.models import Institute


class ListFilter(django_filters.Filter):

    def __init__(self, filter_value=lambda x: x, **kwargs):
        super(ListFilter, self).__init__(**kwargs)
        self.filter_value_fn = filter_value

    def sanitize(self, value_list):
        return [v for v in value_list if v != u'']

    def filter(self, qs, value):
        print(value)
        if value == None:
            return qs
        values = value.split(u",")
        values = self.sanitize(values)
        values = map(self.filter_value_fn, values)
        f = Q()
        for v in values:
            kwargs = {self.field_name: v}
            f = f|Q(**kwargs)
        return qs.filter(f)


class InstituteFilter(django_filters.FilterSet):
    course = django_filters.CharFilter(field_name="course_related__course__name")
    country = ListFilter(field_name="country")
    min_rating = django_filters.NumberFilter(field_name="rating",lookup_expr="gte")
    max_rating = django_filters.NumberFilter(field_name="rating",lookup_expr="lte")
    eligibility = django_filters.CharFilter(field_name="course_related__eligibility")
    max_fee_range = django_filters.NumberFilter(field_name="course_related__total_fee",lookup_expr='lte')
    min_fee_range = django_filters.NumberFilter(field_name="course_related__total_fee",lookup_expr="gte")
    faculty = django_filters.UUIDFilter(field_name="course_related__faculty")
    class Meta:
        model = Institute
        fields = ['course', 'min_rating','min_rating','country', 'city','eligibility','type','faculty']


