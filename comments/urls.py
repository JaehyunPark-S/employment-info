from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("<int:pk>/comment-write/", views.comment_write, name="comment-write"),
    path(
        "<int:comment_pk>/comment-update/",
        views.comment_update,
        name="comment-update",
    ),
    path("<int:pk>/comment-delete/", views.comment_delete, name="comment-delete"),
]
