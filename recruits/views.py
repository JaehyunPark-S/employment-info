from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import render, redirect, reverse
from . import models


class RecruitView(ListView):
    model = models.Recruit
    paginate_by = 12
    paginate_orphans = 1
    ordering = "created"
    context_object_name = "recruits"


def search(request):
    title = request.GET.get("title", " ")
    return render(request, "recruits/search.html", {"title": title})


def autosuggest(request):
    print(request.GET)
    query_original = request.GET.get("term")
    qs = models.Recruit.objects.filter(title__icontains=query_original)
    mylist = []
    mylist += [x.title for x in qs]
    return JsonResponse(mylist, safe=False)
