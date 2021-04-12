from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, reverse, redirect
from . import models
from users import mixins as user_mixins
from users import models as user_model


class HomeView(user_mixins.LoggedInOnlyView, ListView):

    """ HomeView Definition """

    model = models.Board
    template_name = "board_list.html"
    paginate_by = 10
    ordering = "-created"


def search(request):
    host = request.GET.get("host", " ")
    return render(request, "boards/search.html", {"host": host})


def board_like(request, pk):
    board = get_object_or_404(models.Board, pk=pk)
    user = request.user
    me = user_model.User.objects.get(pk=user.pk)

    check_like_board = me.like_boards.filter(pk=pk)
    if check_like_board.exists():
        me.like_boards.remove(board)
        board.like_count -= 1
        board.save()
    else:
        me.like_boards.add(board)
        board.like_count += 1
        board.save()
    return redirect(reverse("core:home"))
