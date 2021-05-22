from django.urls import path
from . import views

app_name = "conversations"

urlpatterns = [
    path("go/<int:a_pk>/<int:b_pk>", views.go_conversations, name="go"),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
    path("list/<int:pk>/", views.ConversationListView.as_view(), name="list"),
    path("list/", views.get_conversation, name="content"),
]
