from django.utils.text import slugify


def upload_student_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.fullname), ext)

    return 'student/profile/{}'.format(
        new_filename
    )
