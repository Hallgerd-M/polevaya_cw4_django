from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Automatically creates superuser"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(email="admin@example.com")
        user.set_password("admin")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
