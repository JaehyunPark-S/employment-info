from django.db import models
from core import models as core_models


class Recruit(core_models.TimeStampedModel):

    """ Room Model Definition" """

    title = models.CharField(max_length=140, null=True)
    company = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    image = models.ImageField()
    host = models.ForeignKey(
        "users.User", related_name="recruit", on_delete=models.CASCADE
    )
