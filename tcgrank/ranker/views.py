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

from ranker.models import RankSite, Tournament, Player, Score, GameAndFormatMeta, CurrentScore, Format
from ranker.forms import UploadForm
from ranker.FileParser import handle_uploaded_file


# helpers

def get_organiser(request):
    if RankSite.objects.filter(site_user=request.user):
        return RankSite.objects.get(site_user=request.user)
    return None


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'ranker/index.html'
    context_object_name = "rank_site_list"
    model = RankSite
    paginate_by = 100


def ranking(request, pk):
    organiser = RankSite.objects.filter(url_name=pk)

    if len(organiser) == 1:
        organiser = organiser[0]

        games_formats = GameAndFormatMeta.objects.filter(organiser=organiser)
        all_game_formats_of_user = {}
        for game_format in games_formats:
            if not game_format.game.game in all_game_formats_of_user.keys():
                all_game_formats_of_user[game_format.game.game] = []
            all_game_formats_of_user[game_format.game.game].append(game_format.format.format)

        for game, formats in all_game_formats_of_user.items():
            game = game
            format = formats[0]
            break

        return HttpResponseRedirect(reverse('rank_game_format', args=[pk, game, format]))
    raise KeyError


def ranking_user_game_format(request, site_name, game, format):
    organiser = RankSite.objects.filter(url_name=site_name)

    if len(organiser) == 1:
        organiser = organiser[0]

        games_formats = GameAndFormatMeta.objects.filter(organiser=organiser)
        all_game_formats_of_user = {}
        for game_format in games_formats:
            if not game_format.game.game in all_game_formats_of_user.keys():
                all_game_formats_of_user[game_format.game.game] = []
            all_game_formats_of_user[game_format.game.game].append(game_format.format.format)

        scores = CurrentScore.objects.filter(organiser=organiser, game=game, format=format).order_by('-current_score','player')

        relevant_formats = all_game_formats_of_user.get(game)
        if relevant_formats is None:
            return HttpResponseRedirect(reverse('index'))
        if len(relevant_formats) > 1:
            relevant_formats.append('Total')
        context = {
            'all_game_formats_of_user': all_game_formats_of_user,
            'relevant_formats': all_game_formats_of_user.get(game),
            'current_game': game,
            'site_name': site_name,
            'scores': scores,
        }

        return render(request, "ranker/user_sub_page.html", context=context)

    raise KeyError

def futurework(request):
    return render(request, "ranker/futurework.html")


def register(request):
    return render(request, "ranker/register.html")


@login_required
def upload(request):
    organiser = get_organiser(request)

    if request.method == 'POST':
        form = UploadForm(request.POST, files=request.FILES)
        if form.is_valid():
            handle_uploaded_file(form, organiser)
            return HttpResponseRedirect(reverse('upload'))#, args=[str(organiser.url_name)]))
    else:
        form = UploadForm()

    # all_formats_pk = list(GameAndFormatMeta.objects.filter(organiser=organiser).values_list('format', flat=True))
    # form.fields['game_format'].queryset = Format.objects.filter(pk__in=all_formats_pk)
    form.fields['game_format'].queryset = GameAndFormatMeta.objects.filter(organiser=organiser)#.values_list('format', flat=True)

    context = {'form': form}
    return render(request, 'ranker/upload.html', context)


class FormatInGameInstanceListView(LoginRequiredMixin, ListView):
    model = GameAndFormatMeta
    context_object_name = 'game_and_format_comb_list'
    template_name = "ranker/mysite.html"

    def get_queryset(self):
        self.organiser = get_organiser(self.request)
        if self.organiser:
            return GameAndFormatMeta.objects.filter(organiser=self.organiser).select_related('format')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FormatInGameInstanceListView, self).get_context_data(**kwargs)
        context.update({'organiser': self.organiser})
        return context


# only for pro users to change the # of tournaments and the time
# class GameFormatCombinationUpdateView(LoginRequiredMixin, UpdateView):
#     model = GameAndFormatMeta
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
