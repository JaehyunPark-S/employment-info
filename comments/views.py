from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse, redirect
from django.http import Http404
from django.contrib import messages
from . import models as comment_model
from boards import models as board_model


@login_required
def comment_write(request, pk):
    write = request.POST.get("comment")
    board = board_model.Board.objects.get(pk=pk)
    user = request.user
    try:
        comment = comment_model.Comment.objects.create(
            comment=write, user=user, board=board
        )
        comment.save()
        messages.success(request, "댓글이 작성되었습니다.")
        return redirect(reverse("core:home"))
    except board_model.Board.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required
def comment_update(request, comment_pk):
    write = request.POST.get("comment")
    user = request.user
    comment = comment_model.Comment.objects.get(pk=comment_pk)
    try:
        if user.pk != comment.user.pk:
            raise Http404()
        comment.comment = write
        comment.save()
        return redirect(reverse("core:home"))
    except comment_model.Comment.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required
def comment_delete(request, pk):
    comment = comment_model.Comment.objects.get(pk=pk)
    user = request.user
    if comment.user != user:
        raise Http404()
    else:
        comment.delete()
        messages.success(request, "댓글이 삭제되었습니다.")
        return redirect(reverse("core:home"))
