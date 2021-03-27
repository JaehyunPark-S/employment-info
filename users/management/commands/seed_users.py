from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import User
from users.models import AttentionLanguage
from users.models import AttentionField
import random


class Command(BaseCommand):

    help = "This command create users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, help="How many users do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        all_users = User.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            int(number),
            {"is_staff": False, "is_superuser": False},
        )
        languages = AttentionLanguage.objects.all()
        fields = AttentionField.objects.all()
        created_users = seeder.execute()
        created_clean = flatten(list(created_users.values()))
        for pk in created_clean:
            user = User.objects.get(pk=pk)
            for l in languages:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    user.att_language.add(l)
            for l in fields:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    user.att_language.add(l)
        self.stdout.write(self.style.SUCCESS(f"{number} Users Created"))
