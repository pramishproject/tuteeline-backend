from django.core.exceptions import ValidationError
import os


def validate_file(value):
    value = str(value).lower()
    if value.endswith(".png") != True and value.endswith(".jpg") != True and value.endswith(".jpeg") != True:
        raise ValidationError("Only PDF and Word Documents can be uploaded")
    else:
        return value


def student_photo(instance, filename):
    upload_dir = os.path.join('student', str(instance.pk))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)


def content_file_name(instance, filename):
    upload_dir = os.path.join('college', str(instance.pk))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)


def facility_file_name(instance, filename):
    upload_dir = os.path.join('college', str(instance.pk))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)


def content_Gallery_name(instance, filename):
    upload_dir = os.path.join('college', str(instance.college_id), 'gallery')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)


def student_certificate(instance, filename):
    upload_dir = os.path.join('student', str(instance.student_id), 'certificate')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)


def student_national_certificate(instance, filename):
    upload_dir = os.path.join('student', str(instance.id), 'certificate')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)


def validate_doc(value):
    value = str(value).lower()
    if value.endswith(".png") != True and value.endswith(".jpg") != True and value.endswith(
            ".jpeg") != True and value.endswith(".pdf") != True and value.endswith(".doc") != True:
        raise ValidationError("Only PDF and Word Documents can be uploaded")
    else:
        return value


def pdfformat(value):
    value = str(value).lower()
    if value.endswith('.pdf') != True:
        raise ValidationError("Only PDF and Word Documents can be uploaded")
    else:
        return value
