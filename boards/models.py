from django.db import models
from core import models as core_models


class Board(core_models.TimeStampedModel):

    """ Room Model Definition" """

    name = models.CharField(max_length=140, null=True)
    description = models.TextField()
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    recommended = models.IntegerField()

    def __str__(self):
        return self.name
