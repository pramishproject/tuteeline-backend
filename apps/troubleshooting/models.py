from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models

# Create your models here.
from apps.consultancy.models import ConsultancyStaff
from apps.core.models import BaseModel
from apps.portal.models import PortalStaff
from apps.user.models import ConsultancyUser


class Troubleshoot(BaseModel):
    STATUS_CHOICES = (
        ("RECEIVED", "Received"),
        ('ASSIGNED', 'Assigned'),
        ('VIEWED', 'Viewed'),
        ('SOLVED', 'Solved'),
        ('ONPROGRESS', 'On progress'),
        ('UNRESOLVED', 'Unresolved'),
    )

    TROUBLESHOOT_CHOICES = (
        ('BILLING', 'Billing'),
        ('TECHNICAL', 'Technical'),)
    description = models.TextField()
    assigned_by = models.ForeignKey(ConsultancyStaff, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(
        PortalStaff,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='RECEIVED'
    )
    troubleshoot_type = models.CharField(max_length=10,choices=TROUBLESHOOT_CHOICES)


    def __str__(self):
        return f' Task added by {self.assigned_by} to {self.assigned_to} ' \
               f'with status-{self.status} '


class BillingTroubleshoot(BaseModel):
    trouble_shot = models.OneToOneField(Troubleshoot, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f' Task added by {self.trouble_shot.assigned_by} to {self.trouble_shot.assigned_to} ' \
               f'with status-{self.trouble_shot.status} '

    def clean(self):
        if not self.trouble_shot.troubleshoot_type == 'BILLING':
            raise DjangoValidationError({
                'trouble_shot': 'Trouble shot type  must be billing.'
            })
