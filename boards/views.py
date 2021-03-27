from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_boards(request):
    page = int(request.GET.get("page", 1))
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_boards = models.Board.objects.all()[offset:limit]
    page_count = ceil(models.Board.objects.count() / page_size)
    return render(
        request,
        "boards/home.html",
        context={
            "boards": all_boards,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )
