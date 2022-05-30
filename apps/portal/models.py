from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.staff.models import StaffPosition
from apps.user.models import PortalUser


class PortalStaff(BaseModel):
    user = models.OneToOneField(PortalUser, on_delete=models.CASCADE)
    role = models.ForeignKey(StaffPosition, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

    def clean(self):
        if self.role.name == 'owner':
            if PortalStaff.objects.filter(
                    role__name__iexact='owner',
            ).exists():
                raise DjangoValidationError(
                    {'name': _('Cannot Assign two owners.')}
                )
