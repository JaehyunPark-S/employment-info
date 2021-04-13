from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    # path("board-like/<int:pk>/", views.board_like, name="board-like")
    path("board-like/", views.board_like, name="board-like"),
]
