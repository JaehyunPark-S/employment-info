import json
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, FormView, UpdateView
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.contrib import messages
from . import models, forms
from users import mixins as user_mixins
from users import models as user_model


class HomeView(user_mixins.LoggedInOnlyView, ListView):

    """ HomeView Definition """

    model = models.Board
    template_name = "board_list.html"
    paginate_by = 10
    ordering = "-created"


class BoardCreatView(FormView):
    template_name = "boards/board_create.html"
    form_class = forms.BoardCreateForm
    success_url = reverse_lazy("core:home")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["description"].label = "글 내용"
        return form


class UpdateBoardView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Board
    template_name = "boards/board_update.html"
    fields = ("description",)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["description"].label = "글 내용"
        return form

    def get_object(self, queryset=None):
        board = super().get_object(queryset=queryset)
        if board.host.pk != self.request.user.pk:
            raise Http404()
        return board


@login_required
def board_create(request):
    description = request.POST.get("description")
    user = request.user
    board = models.Board.objects.create(description=description, host=user)
    board.save()
    messages.success(request, "게시글이 작성되었습니다.")
    return redirect(reverse("core:home"))


@login_required
def board_update(request):
    description = request.POST.get("description")
    pk = request.POST.get("pk")
    board = models.Board.objects.get(pk=pk)
    user = request.user
    try:
        if user.pk != board.host.pk:
            raise Http404()
        board.description = description
        board.save()
        return redirect(reverse("core:home"))
    except models.Board.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required
def board_delete(request, pk):
    user = request.user
    try:
        board = models.Board.objects.get(pk=pk)
        if board.host.pk != user.pk:
            messages.error(request, "잘못된 요청입니다.")
        else:
            board.delete()
            messages.success(request, "게시글이 삭제되었습니다.")
            return redirect(reverse("core:home"))
    except models.Board.DoesNotExist:
        return redirect(reverse("core:home"))


def search(request):
    host = request.GET.get("host", " ")
    return render(request, "boards/search.html", {"host": host})


@login_required
@require_POST
def board_like(request):
    pk = request.POST.get("pk", None)
    board = get_object_or_404(models.Board, pk=pk)
    user = request.user
    me = user_model.User.objects.get(pk=user.pk)

    check_like_board = me.like_boards.filter(pk=pk)

    if check_like_board.exists():
        me.like_boards.remove(board)
        if board.like_count == 0:
            board.like_count = 0
        else:
            board.like_count -= 1
        board.save()
        message = "좋아요 취소"
        icon = '<i class="far fa-heart mb-2 mx-1.5 text-red-400"></i>'
    else:
        me.like_boards.add(board)
        board.like_count += 1
        board.save()
        message = "좋아요"
        icon = '<i class="fas fa-heart mb-2 mx-1.5 text-red-400"></i>'

    context = {"like_count": board.like_count, "message": message, "icon": icon}
    return HttpResponse(json.dumps(context), content_type="application/json")


# # DJANGO LIKE
# def board_like(request, pk):
#     board = get_object_or_404(models.Board, pk=pk)
#     user = request.user
#     me = user_model.User.objects.get(pk=user.pk)

#     check_like_board = me.like_boards.filter(pk=pk)
#     if check_like_board.exists():
#         me.like_boards.remove(board)
#         board.like_count -= 1
#         board.save()
#     else:
#         me.like_boards.add(board)
#         board.like_count += 1
#         board.save()
#     return redirect(reverse("core:home"))
