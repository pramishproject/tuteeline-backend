

from django.utils.text import slugify


def upload_voucher_icon(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.name), ext)

    return 'payment/icon/{}'.format(
        new_filename
    )