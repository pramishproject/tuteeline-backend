from django.utils.text import slugify
def upload_linkage_docs(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.student), ext)

    return 'student/document/{}'.format(
        new_filename
    )