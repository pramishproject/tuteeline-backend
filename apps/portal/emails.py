import uuid

from templated_mail.mail import BaseEmailMessage


class SendEmailToPortalStaff(BaseEmailMessage):
    template_name = 'email/consultancy_staff_welcome.html'

