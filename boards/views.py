from django.views.generic import ListView
from django.shortcuts import render
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Board
    template_name = "board_list.html"
    paginate_by = 10
    ordering = "created"


def search(request):
    description = request.GET.get("description", " ")
    return render(request, "boards/search.html", {"description": description})
