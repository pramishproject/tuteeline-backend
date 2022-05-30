
import uuid

from templated_mail.mail import BaseEmailMessage


class SendEmailToStudent(BaseEmailMessage):
    template_name = 'email/student_email_verification.html'