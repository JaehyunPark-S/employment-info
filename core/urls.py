from django.urls import path
from boards import views as board_views

app_name = "core"

urlpatterns = [
    path("", board_views.HomeView.as_view(), name="home"),
]
