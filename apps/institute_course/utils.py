from django.db.models import Count
from django.db.models.functions import TruncDay

from apps.institute_course.models import InstituteApply


def get_student_application_status(student_id):
    application=InstituteApply.objects.filter(
        student=student_id
        # created_at__range=["2021-12-01", "2022-01-31"]
    ).annotate(date=TruncDay('created_at')).values("date", "action"). \
        annotate(action_count=Count('action'))

    print(application)
    return application