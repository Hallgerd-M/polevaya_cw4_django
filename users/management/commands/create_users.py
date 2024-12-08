from django.core.management.base import BaseCommand
from django.core.management import call_command


class ManagerCommand(BaseCommand):
    help = "Add users as managers"

    def handle(self, *args, **kwargs):
        call_command('load_data', 'managers_fixture.json')
        self.stdout.write(self.style.SUCCESS('Data from fixture successfully loaded'))
