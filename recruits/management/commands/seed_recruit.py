from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users import models as user_models
from recruits import models as recruit_models
import random


class Command(BaseCommand):

    help = "This command create recruit"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many recruit do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        all_users = user_models.User.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            recruit_models.Recruit,
            number,
            {
                "name": lambda x: seeder.faker.name(),
                "host": lambda x: random.choice(all_users),
                "enterprise": lambda x: seeder.faker.name(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Recruit Created"))
