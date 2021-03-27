from django.urls import path
from boards import views as board_views

app_name = "core"

urlpatterns = [
    path("", board_views.all_boards, name="home"),
]
