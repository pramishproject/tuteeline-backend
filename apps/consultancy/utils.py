from django.utils.text import slugify


def upload_consultancy_logo_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'consultancy/logo/{}'.format(
        new_filename
    )


def upload_consultancy_cover_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'consultancy/cover_image/{}'.format(
        new_filename
    )


def upload_consultancy_staff_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.consultancy), ext)

    return 'consultancy/staff_image/{}'.format(
        new_filename
    )

