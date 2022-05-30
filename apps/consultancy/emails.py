import uuid

from templated_mail.mail import BaseEmailMessage


class SendEmailToConsultanySTaff(BaseEmailMessage):
    template_name = 'email/consultancy_staff_welcome.html'

