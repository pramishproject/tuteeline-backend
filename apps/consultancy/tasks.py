from apps.consultancy import emails
from config.celery_app import app


@app.task(ignore_result=True)
def send_set_password_email_to_user(**kwargs):
    return emails.SendEmailToConsultanySTaff(context=kwargs).send(to=[kwargs['user_email']])

