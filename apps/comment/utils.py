from django.utils.text import slugify
def upload_comment_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'application/comment/{}'.format(
        new_filename
    )