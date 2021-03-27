from django.views.generic import ListView
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Board
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
