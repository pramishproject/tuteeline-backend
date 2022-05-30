from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.usecases import User
from apps.user.models import NormalUser


@receiver(post_save, sender=User)
def create_normal_user(sender, instance, **kwargs):
    user = instance
    if user.is_staff and not user.is_staff:
        if not hasattr(user, 'normaluser'):
            NormalUser.objects.create(user=user)


@receiver(post_save, sender=NormalUser)
def archive_normal_user(sender, instance, **kwargs):
    user = instance.user
    user.is_archived = instance.is_archived
    user.save()
