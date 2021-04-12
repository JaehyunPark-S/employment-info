from django.db import models
from core import models as core_models


class Board(core_models.TimeStampedModel):

    """ Room Model Definition" """

    description = models.TextField()
    host = models.ForeignKey(
        "users.User", related_name="board", on_delete=models.CASCADE
    )
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.host.email
