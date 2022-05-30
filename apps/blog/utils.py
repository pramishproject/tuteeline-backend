from django.utils.text import slugify


def upload_blog_image_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.title), ext)

    return 'blog/{}'.format(
        new_filename
    )