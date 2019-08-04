from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from ranker.models import RankSite, Tournament, Player, Score, GameFormatCombination, CurrentScore
from ranker.forms import UploadForm
from ranker.FileParser import handle_uploaded_file

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'ranker/index.html'
    context_object_name = "rank_site_list"
    model = RankSite
    paginate_by = 100


def ranking(request, pk):
    # todo https://stackoverflow.com/questions/7287027/displaying-a-table-in-django-from-database
    return render(request, "ranker/index.html")


def futurework(request):
    return render(request, "ranker/futurework.html")


def register(request):
    return render(request, "ranker/register.html")


@login_required
def upload(request):

    if request.method == 'POST':
        form = UploadForm(request.POST, files=request.FILES)
        if form.is_valid():
            handle_uploaded_file(request)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UploadForm()

    context = {'form': form}
    return render(request, 'ranker/upload.html', context)


class GameFormatCombinationListView(LoginRequiredMixin, ListView):
    model = GameFormatCombination
    context_object_name = 'game_and_format_comb_list'
    template_name = "ranker/mysite.html"

    def get_queryset(self):
        organiser = RankSite.objects.get(site_user=self.request.user)
        if organiser:
            return GameFormatCombination.objects.filter(organiser=organiser)


# only for pro users to change the # of tournaments and the time
# class GameFormatCombinationUpdateView(LoginRequiredMixin, UpdateView):
#     model = GameFormatCombination
#     fields = ('game', 'format')
#     success_url = reverse_lazy('mysite')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('mysite')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ranker/change_password.html', {
        'form': form
    })
