from apps.institute import models
from django.utils.datetime_safe import datetime
from django.utils.text import slugify
from datetime import date

def upload_institute_staff_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.institute), ext)

    return 'institute/staff_image/{}'.format(
        new_filename
    )

def upload_institute_logo_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'institute/logo/{}'.format(
        new_filename
    )


def upload_institute_cover_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'institute/cover_image/{}'.format(
        new_filename
    )

def upload_brochure(instance,filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'institute/cover_image/{}'.format(
        new_filename
    )

def past_date(value):
    if value > date.today():
        raise models.DjangoValidationError("the date cannot be in the future")
    return value


def upload_facility_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'facility/icon/{}'.format(
        new_filename
    )
