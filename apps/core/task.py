from apps.core import email
from config.celery_app import app



@app.task(ignore_result=True)
def send_set_confirmation_email_to_user(**kwargs):
    return email.SendConfirmationEmail(context=kwargs).send(to=[kwargs['user_email']])