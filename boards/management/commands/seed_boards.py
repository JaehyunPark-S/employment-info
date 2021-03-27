from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users import models as user_models
from boards import models as board_models
import random


class Command(BaseCommand):

    help = "This command create boards"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many boards do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        all_users = user_models.User.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            board_models.Board,
            number,
            {
                "name": lambda x: seeder.faker.name(),
                "host": lambda x: random.choice(all_users),
                "recommended": lambda x: random.randint(0, 500),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Boards Created"))
