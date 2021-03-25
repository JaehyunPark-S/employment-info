from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.AttentionField)
class ItemAdmin(admin.ModelAdmin):

    pass


@admin.register(models.AttentionLanguage)
class ItemAdmin(admin.ModelAdmin):

    pass


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Cunstom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "att_field",
                    "att_language",
                    "followers",
                    "followings",
                )
            },
        ),
    )
