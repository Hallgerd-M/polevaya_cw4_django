from django.core.management.base import BaseCommand

from message_sending.services.send_mail import EmailService


class Command(BaseCommand):
    help = "Send messages by users"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="Id рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        EmailService().send_message(mailing_id)
