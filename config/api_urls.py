from django import urls
from apps import activity, studentIdentity
from django.urls import path, include

# This file will contain all the end-points
urlpatterns = [
    # path(
    #     '',
    #     include('apps.college.urls')
    # ),
    # path(
    #     'student/',
    #     include('apps.student.urls')
    # ),
    path(
        'notification/',
        include('apps.notification.urls'),
    ),
    path(
        'students/',
        include('apps.students.urls')
    ),
    path(
        'consultancy/',
        include('apps.consultancy.urls')
    ),
    path(
        'institute/',
        include('apps.institute.urls')
    ),
    path(
        'institute_course/',
        include('apps.institute_course.urls')
    ),
    path(
        'auth/',
        include('apps.auth.urls')
    ),
    path(
        'staff/',
        include('apps.staff.urls')
    ),
    path(
        'portal/',
        include('apps.portal.urls')
    ),
    path(
        'setting/',
        include('apps.settings.urls')
    ),
    path(
        'troubleshooting/',
        include('apps.troubleshooting.urls')
    ),
    path(
        'schedule/',
        include('apps.schedule.urls')
    ),
    path(
        'blogs/',
        include('apps.blog.urls')
    ),
    path(
        'gallery/',
        include('apps.gallery.urls')
    ),
    path(
        'student_identity/',
        include('apps.studentIdentity.urls')
    ),
    path(
        'academic/',
        include('apps.academic.urls')
    ),
    path(
        'parents/',
        include('apps.parentsDetail.urls')
    ),
    path(
        'language/',
        include('apps.language.urls')
    ),
    path(
        'activities/',
        include('apps.activity.urls')
    ),
    path(
        'review/',
        include('apps.review.urls')
    ),
    path(
        'councelling/',
        include('apps.counselling.urls')
    ),
    # path(
    #     'location/',
    #     include('apps.geo_location.urls')
    # )
]
