from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("recruit-like/", views.recruit_like, name="recruit-like"),
]
