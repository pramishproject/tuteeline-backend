from django.utils.text import slugify


def upload_student_identity_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.student), ext)

    return 'student/identity/{}'.format(
        new_filename
    )