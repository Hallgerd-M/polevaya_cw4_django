from django.core.mail import send_mail

from config.settings import (EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER,
                             EMAIL_PORT)
from message_sending.models import Log, Mailing


class EmailService:

    def __init__(self):
        self.smtp_server = EMAIL_HOST
        self.smtp_port = EMAIL_PORT
        self.smtp_username = EMAIL_HOST_USER
        self.smtp_password = EMAIL_HOST_PASSWORD

    def send_message(self, mailing_id):
        mailing = Mailing.objects.filter(id=mailing_id).first()
        letter = mailing.message
        subject = letter.subject
        message = letter.body
        from_email = self.smtp_username
        recipient_list = list(mailing.addressee.values_list("email", flat=True))
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
            )
            create_log(mailing_id, status=Log.SUCCESSFULL)
            print("ok")
        except Exception as e:
            create_log(mailing_id, status=Log.UNSUCCESSFULL, answer=str(e))
            print(e)


def create_log(mailing_id, status, answer="Delivered"):
    Log.objects.create(mailing_id=mailing_id, status=status, answer=answer)
