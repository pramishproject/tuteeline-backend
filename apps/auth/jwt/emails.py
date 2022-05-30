import uuid

from templated_mail.mail import BaseEmailMessage


class EmailVerificationEmail(BaseEmailMessage):
    template_name = 'email/two_fa.html'
    #
    # def get_context_data(self):
    #     context = super(EmailVerificationEmail, self).get_context_data()
    #     context['code'] = context.get('code')
    #     # return context
