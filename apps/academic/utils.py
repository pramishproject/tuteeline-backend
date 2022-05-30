from django.utils.text import slugify

def check_score(sender, instance, *args, **kwargs):
    if instance.score > instance.full_score:
        raise ValueError("score cannot be grater then full score")

def upload_academic_doc_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % (slugify(instance.student), ext)

    return 'student/document/{}'.format(
        new_filename
    )