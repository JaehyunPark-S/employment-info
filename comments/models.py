from django.db import models
from core import models as core_models


class Comment(core_models.TimeStampedModel):

    """ Comment Model Definition """

    comment = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="comment", on_delete=models.CASCADE
    )
    board = models.ForeignKey(
        "boards.Board", related_name="comment", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.comment} - {self.board}"
