from django.urls import path
from . import views

app_name = "recruits"

urlpatterns = [
    path("info/", views.RecruitView.as_view(), name="info"),
]
