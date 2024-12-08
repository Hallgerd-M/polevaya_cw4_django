from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from message_sending.models import Message


def send_message(message_id, user_email):
    letter = Message.objects.filter(message_id=message_id)
    subject = letter.subject
    message = letter.message
    from_email = EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
