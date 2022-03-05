from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
import uuid

from user.models import User


class Command(BaseCommand):
    help="Replace django createsuperuser command"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('username')
        parser.add_argument('password')

        # Named (optional) arguments
        parser.add_argument('--email', default='')

    def handle(self, *args, **options):
        user = User.objects.create(
            id=uuid.uuid4(),
            username=options['username'],
            password=make_password(options['password'], 'pbkdf2_sha256'),
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )
        user.save()

