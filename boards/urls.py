from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    # path("board-create/", views.BoardCreatView.as_view(), name="board-create"),
    path("board-create/", views.board_create, name="board-create"),
    # path(
    #     "<int:pk>/board-update/", views.UpdateBoardView.as_view(), name="board-update"
    # ),
    path("update/", views.board_update, name="board-update"),
    path("<int:pk>/delete/", views.board_delete, name="board-delete"),
    path("board-like/", views.board_like, name="board-like"),
]
