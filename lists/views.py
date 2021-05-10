import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import reverse, get_object_or_404, redirect
from django.http import HttpResponse
from recruits import models as recruit_models
from . import models


@login_required
@require_POST
def recruit_like(request):
    pk = request.POST.get("pk", None)
    recruit = get_object_or_404(recruit_models.Recruit, pk=pk)
    user = request.user

    the_list, created = models.List.objects.get_or_create(user=user, name="Fav Recruit")
    check_like_recruit = the_list.recruits.filter(pk=pk)
    if check_like_recruit.exists():
        the_list.recruits.remove(recruit)
        icon = '<i class="far fa-heart mb-2 text-red-400"></i>'
    else:
        the_list.recruits.add(recruit)
        icon = '<i class="fas fa-heart mb-2 text-red-400"></i>'
    context = {"icon": icon}
    return HttpResponse(json.dumps(context), content_type="application/json")
