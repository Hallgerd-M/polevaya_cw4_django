from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class ModeratorCommand(BaseCommand):
    help = "Add users as manager"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.create(email="example@example.com")
        user.set_password("123qwe")
        user.is_active = True
        user.is_staff = True

        managers_group = Group.objects.get(name="Managers")
        user.groups.add(managers_group)

        user.save()
