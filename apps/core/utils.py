import os

from django.utils import timezone
from django.utils.timezone import now
from rest_framework.utils import model_meta


def generate_custom_id(initial: str, model):
    try:
        last_record = model.objects.last()

        if len(last_record.id) > len(initial):
            next_id = int(last_record.id[len(initial):]) + 1
        else:
            next_id = int(last_record.id) + 1

        last_record_id = '{0:04}'.format(
            next_id
        )
        custom_id = '{}{}'.format(
            initial,
            last_record_id
        )
    except model.DoesNotExist:
        custom_id = '{}0001'.format(
            initial,
        )

    return custom_id


def last_id_for_bulk_create(initial: str, model):
    try:
        last_record = model.objects.last()
        return int(last_record.id[len(initial):])
    except model.DoesNotExist:
        return 0


def update(instance, data):
    info = model_meta.get_field_info(instance)

    for attr, value in data.items():
        if attr in info.relations and info.relations[attr].to_many:
            field = getattr(instance, attr)
            field.set(value)
        else:
            setattr(instance, attr, value)
    instance.updated = timezone.now()
    instance.save()


def generate_filename(filename, keyword):
    """
    Generates filename with uuid and a keyword
    :param filename: original filename
    :param keyword: keyword to be added after uuid
    :return: new filename in string
    """
    ext = filename.split('.')[-1]
    new_filename = "%s_%s.%s" % (keyword, now().strftime("%Y%m%d-%H%M%S"), ext)
    return new_filename


def upload_to_folder(instance, filename, folder, keyword):
    """
    Generates the path where it should to uploaded

    :param instance: model instance
    :param filename: original filename
    :param folder: folder name where it should be stored
    :param keyword: keyword to be attached with uuid
    :return: string of new path
    """
    return os.path.join(folder, generate_filename(
        filename=filename,
        keyword=keyword
    ))
