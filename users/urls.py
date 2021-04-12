from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>/", views.complete_verification, name="complete-verfication"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update-profile/", views.UpdatePasswordView.as_view(), name="password"),
    path("update-password/", views.UpdateProfileView.as_view(), name="update"),
    path("update-avatar/", views.UpdateAvatarView.as_view(), name="avatar"),
    path("<int:pk>/delete-avatar/", views.delete_avatar, name="delete-avatar"),
    path("add-follow/<int:pk>/", views.add_follow, name="add-follow"),
    path("delete-follow/<int:pk>/", views.delete_follow, name="delete-follow"),
]
