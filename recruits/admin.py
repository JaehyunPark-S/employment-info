from django.contrib import admin
from . import models


@admin.register(models.Recruit)
class RecuritAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "location",
        "link",
    )
