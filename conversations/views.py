import json
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from django.http import HttpResponse
from users import models as user_models
from . import models, forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def go_conversations(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        conversation = models.Conversation.objects.filter(
            participants__in=[user_one]
        ).filter(participants__in=[user_two])
        if conversation.count() == 0:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
            conversation = models.Conversation.objects.filter(
                participants__in=[user_one]
            ).filter(participants__in=[user_two])
        return redirect(
            reverse("conversations:detail", kwargs={"pk": conversation[0].pk})
        )


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        form = forms.AddCommentForm()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation, "form": form},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))


class ConversationListView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.filter(participants=pk)
        if not conversation:
            raise Http404()
        form = forms.AddCommentForm()
        return render(
            self.request,
            "conversations/conversation_list.html",
            {"conversation": conversation, "form": form},
        )


@login_required
@require_POST
def get_conversation(request):
    pk = request.POST.get("pk", None)
    conversation = models.Conversation.objects.get(pk=pk)
    if conversation is None:
        pass
    return HttpResponse(json.dumps(conversation), content_type="application/json")
