from django.shortcuts import render
from django.views import generic

from ranker.models import RankSite, Tournament, Player, Score, GameAndFormat, CurrentScores
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'ranker/index.html'
    context_object_name = "rank_site_list"
    model = RankSite
    paginate_by = 1

    # todo https://stackoverflow.com/questions/7287027/displaying-a-table-in-django-from-database


def ranking(request, pk):

    return render(request, "ranker/index.html")


def futurework(request):
    return render(request, "ranker/futurework.html")
