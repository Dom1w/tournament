from django.core.validators import RegexValidator

from defusedxml.ElementTree import parse
import datetime

from ranker.models import Tournament, Player, Score, CurrentScore, GameAndFormatMeta

alphabetic = RegexValidator(r'^[a-zäöü]+$', message='Only alphabetic characters are allowed.')


def validate_date(date_text):
    import datetime
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def handle_uploaded_file(form, organiser):
    file_format = form.cleaned_data['file_format']

    if int(file_format) == 1:  # TCGRanks.com Format
        raise NotImplementedError

    elif int(file_format) == 2:  # Magic Tournament Software
        return parse_magic_tournament_software(form, organiser)

    elif int(file_format) == 3:  # Yu-Gi-Oh Tournament Software
        return parse_yugioh_tournament_software(form, organiser)
    # try except - wrong file

    raise ValueError("Wrong File Format")
    pass


def parse_magic_tournament_software(form, organiser):
    # sorted_players = sorted(all_players.items(), key=lambda item: (item[1]['wins'], -item[1]['losses'], item[1]['draws']), reverse=True)
    raise NotImplementedError


def parse_yugioh_tournament_software(form, organiser):
    game_and_format = form.cleaned_data['game_format']

    file = form.cleaned_data['file']

    et = parse(file)
    root = et.getroot()

    date = root.find('Date').text
    validate_date(date)

    all_players = {}
    for player in root.find('TournamentPlayers').findall('TournPlayer'):
        player_details = player.find('Player')
        player_game_id = int(player_details.find('ID').text)
        player_first_name = player_details.find('FirstName').text
        player_last_name = player_details.find('LastName').text
        player_rank = int(player.find('Rank').text)

        alphabetic(player_first_name.lower())
        alphabetic(player_last_name.lower())

        p, created = Player.objects.get_or_create(organiser=organiser, first_name= player_first_name, last_name=player_last_name, game_id=player_game_id)
        all_players[player_game_id] = {'wins': 0, 'draws': 0, 'losses': 0, 'rank': player_rank, 'player': p}

    for match in root.find('Matches').findall('TournMatch'):
        players = match.findall('Player')
        winner = int(match.find('Winner').text)

        if match.find('Status').text == 'Winner':
            players = [int(players[0].text), int(players[1].text)]
            players.remove(winner)
            loser = players[0]

            all_players[winner]['wins'] += 1
            if loser != 0:
                all_players[loser]['losses'] += 1

        # todo implement draws

    t = Tournament(date=date, game_and_format=game_and_format)
    t.save()

    for key, value in all_players.items():
        s = Score(tournament=t, player=value['player'], wins=value['wins'], draws=value['draws'], losses=value['losses'],
              rank=value['rank'])
        s.save()

    calculate_current_scores(organiser)

    pass


def calculate_current_scores(organiser):
    CurrentScore.objects.filter(organiser=organiser).delete()

    all_game_format_metas = GameAndFormatMeta.objects.filter(organiser=organiser)

    total_scores = {} # magic: player: score

    for game_format in all_game_format_metas:

        valid_after_date = datetime.date.today()-datetime.timedelta(days=game_format.max_time_back)

        tournaments = Tournament.objects.filter(game_and_format=game_format).filter(date__gte=valid_after_date)
        tournaments = tournaments.order_by('-date')[:game_format.number_of_tournaments_to_be_counted]

        player_scores = {}
        for tournament in tournaments:
            scores = Score.objects.filter(tournament=tournament)
            for score in scores:
                tournament_score = score.wins * tournament.points_per_win + score.draws * tournament.points_per_draw + score.losses * -tournament.minus_points_per_loss + tournament.points_for_attendance
                if score.player not in player_scores:
                    player_scores[score.player] = 0
                player_scores[score.player] += tournament_score
                if score.rank == 1:
                    player_scores[score.player] += tournament.points_for_rank_one

        for player, current_score in player_scores.items():
            cs = CurrentScore(organiser=organiser, game=game_format.game.game, format=game_format.format.format, player=player, current_score=current_score)
            cs.save()

            # game - player - score
            if game_format.game.game not in total_scores.keys():
                total_scores[game_format.game.game] = {}
            if player not in total_scores[game_format.game.game].keys():
                total_scores[game_format.game.game][player] = 0
            total_scores[game_format.game.game][player] += current_score

    for game in total_scores:
        for player, score in total_scores[game].items():
            cs = CurrentScore(organiser=organiser, game=game, format='Total', player=player, current_score=score)
            cs.save()

    pass
