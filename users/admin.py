from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.AttentionLanguage, models.AttentionField)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.users.count()

    pass


@admin.register(models.FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    list_display = (
        "follower",
        "count_follower",
    )

    def count_follower(self, obj):
        return obj.following.count()


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
                    "login_method",
                    "followings",
                    "like_boards",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "email",
        "count_att_field",
        "count_att_language",
        "email_verified",
        "login_method",
        "count_followings",
    )

    filter_horizontal = (
        "att_field",
        "att_language",
        "followings",
    )

    def count_att_field(self, obj):
        return obj.att_field.count()

    def count_att_language(self, obj):
        return obj.att_language.count()

    def count_followings(self, obj):
        return obj.followings.count()
