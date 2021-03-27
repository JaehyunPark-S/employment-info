from django.shortcuts import render
from . import models


def login_view(request):
    all_boards = models.User.objects.all()
    return render(request, "login_view")
