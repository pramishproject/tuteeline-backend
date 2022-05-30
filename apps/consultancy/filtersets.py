from django_filters import rest_framework as filters, BaseInFilter


class ConsultancyStaffSearchFilter(filters.FilterSet):
    role = filters.CharFilter(
        field_name="role__name",
        label='role'
    )
    email = filters.CharFilter(
        field_name="email",
        label='email'
    )
    fullname = filters.CharFilter(
        field_name="user__fullname",
        label='fullname'
    )

    class Meta:
        fields = (
            'role',
            'fullname',
            'email',
        )
