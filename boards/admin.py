from django.contrib import admin
from . import models


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):

    """ Board Admin Definition """

    list_display = (
        "host",
        "like_count",
    )

    raw_id_fields = ("host",)
