from django.urls import path
from . import views

app_name = "recruits"

urlpatterns = [
    path("", views.RecruitView.as_view(), name="info"),
    path("search/", views.search, name="search"),
    path("autosuggest/", views.autosuggest, name="autosuggest"),
]
