from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import render, redirect, reverse
from . import models, tasks
from math import ceil

# import pandas as pd
# import csv

# user = user_models.User.objects.get(username="jaehyun@jj.hh")
# with open("recruits/jobs.csv", "r") as f:
#     dr = csv.DictReader(f)
#     s = pd.DataFrame(dr)
# ss = []
# for i in range(len(s)):
#     if s["image"][i] == "":
#         s["image"][i] = "../static/img/company.png"
#     st = (s["title"][i], s["company"][i], s["location"][i], s["link"][i], s["image"][i])
#     ss.append(st)

# for i in range(len(s)):
#     models.Recruit.objects.create(
#         title=ss[i][0],
#         company=ss[i][1],
#         location=ss[i][2],
#         link=ss[i][3],
#         image=ss[i][4],
#         host=user,
#     )

# tasks.so_crawler()


class RecruitView(ListView):
    model = models.Recruit
    paginate_by = 10
    paginate_orphans = 1
    ordering = "created"
    context_object_name = "recruits"


def search(request):
    page = int(request.GET.get("page", 1))
    page = int(page or 1)
    page_size = 20
    limit = page_size * page
    offset = limit - page_size
    qs = models.Recruit.objects.all()
    title = request.GET.get("q")
    if title:
        qs = qs.filter(title__contains=title)
    page_count = qs.count() / page_size
    qs = qs[offset:limit]

    return render(
        request,
        "recruits/search.html",
        {"recruits": qs, "title": title, "page": page, "page_count": ceil(page_count)},
    )


def autosuggest(request):
    query_original = request.GET.get("term")
    qs = models.Recruit.objects.filter(title__icontains=query_original)
    mylist = []
    mylist += [x.title for x in qs]
    return JsonResponse(mylist, safe=False)
