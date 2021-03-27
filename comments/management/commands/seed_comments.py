from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from boards import models as board_models
from comments import models as comment_models
import random


class Command(BaseCommand):

    help = "This command create comments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many comments do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        all_users = user_models.User.objects.all()
        all_boards = board_models.Board.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            comment_models.Comment,
            number,
            {
                "user": lambda x: random.choice(all_users),
                "board": lambda x: random.choice(all_boards),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Comments Created"))
