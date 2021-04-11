import os
import requests
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(f"{user.login_method}로그인을 이용해 주세요.")
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("정보가 존재하지 않습니다.")
        else:
            raise GithubException("코드가 존재하지 않습니다.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account", None)
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("이메일을 찾을 수 없습니다.")
        nickname = kakao_account.get("profile").get("nickname")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"{user.login_method}로그인을 이용해 주세요.")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(mixins.LoggedInOnlyView, DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "gender",
        "bio",
        "att_field",
        "att_language",
    )

    success_message = "프로필 수정완료"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].label = "이름"
        form.fields["gender"].label = "성별"
        form.fields["bio"].label = "자기소개"
        form.fields["att_field"].label = "관심 분야"
        form.fields["att_language"].label = "관심 언어"
        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView
):

    template_name = "users/update-password.html"
    success_message = "비밀번호 변경완료"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].label = "이전 비밀번호"
        form.fields["new_password1"].label = "새로운 비밀번호"
        form.fields["new_password2"].label = "비밀번호 확인"
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class UpdateAvatarView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-avatar.html"
    fields = ("avatar",)

    def get_object(self, queryset=None):
        return self.request.user


def delete_avatar(request, pk):
    user = models.User.objects.get(pk=pk)
    user.avatar = None
    user.save()
    return redirect(reverse("users:profile", kwargs={"pk": pk}))
