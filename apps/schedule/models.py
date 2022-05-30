from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from apps.consultancy.models import ConsultancyStaff
from apps.core.models import BaseModel
from apps.user.models import StudentUser

User = get_user_model()


class CounsellingSchedule(BaseModel):
    COUNSELLOR_STATUS = (
        ('AVAILABLE', 'Available'),
        ('BUSY', 'Busy'),
        ('UNAVAILABLE', 'Unavailable')
    )
    counsellor = models.ForeignKey(to=ConsultancyStaff, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    location = models.CharField(max_length=100)
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=COUNSELLOR_STATUS)

    def clean(self):
        import datetime
        datetime.datetime.now()
        if self.date<datetime.datetime.now().date():
            raise DjangoValidationError(
                {
                    'date': _('Past date cannot be added.')
                }
            )
        if self.counsellor.role.name != 'counsellor':
            raise DjangoValidationError(
                {
                    'counsellor': _('Only counselor staff can be added')
                }
            )
        if self.end_time < self.start_time:
            raise DjangoValidationError(
                {
                    'end_time': _('End time must be greater than start time')
                }
            )

    def __str__(self):
        return self.title


class Booking(BaseModel):
    schedule = models.OneToOneField(to=CounsellingSchedule, on_delete=models.CASCADE)
    user = models.ForeignKey(to=StudentUser, on_delete=models.CASCADE)
    note = models.TextField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'

    # def clean(self):
    #     if self.user.user_type != 'student_user':
    #         raise DjangoValidationError(
    #             {
    #                 'user': _('User must be student to book schedule.')
    #             }
    #         )
