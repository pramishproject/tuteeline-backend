import uuid

from templated_mail.mail import BaseEmailMessage


class SendConfirmationEmail(BaseEmailMessage):
    template_name = 'email/confirmation_email.html'