from django.utils.text import slugify


def upload_portal_user_cover_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'portal/profile_pictures/{}'.format(
        new_filename
    )
