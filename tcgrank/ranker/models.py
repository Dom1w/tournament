from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.urls import reverse
# from django.contrib.postgres.fields import JSONField

import datetime

# Create your models here.
alpha_numeric = RegexValidator(r'^[0-9a-zA-Z\-]+$', message='Only alphanumeric characters are allowed.')


validator_fn = [
    alpha_numeric,
    RegexValidator(r'^(?!admin|futurework|upload|mysite|accounts|gameandformat).*', "Website relevant url. You cannot use it.")
]


def regex_validators(value):
    for validator in validator_fn:
        validator(value.lower())
    return value


class RankSite(models.Model):
    site_user = models.OneToOneField(User, on_delete=models.CASCADE)
    url_name = models.CharField(max_length=50, help_text="Enter a name for you sub-url of tcgrank", primary_key=True,
                                validators=[regex_validators])
    homepage = models.URLField(default="http://127.0.0.1:8000/register", help_text="Enter a url to your homepage")

    SUBSCRIPTION_LEVEL = (
        ('f', 'Free'),
        ('p', 'Pro'),
        ('u', 'Ultimate'),
    )

    subscription = models.CharField(
        max_length=1,
        choices=SUBSCRIPTION_LEVEL,
        default='f',
        help_text='Subscription of User',
    )

    class Meta:
        ordering = ['url_name']

    def __str__(self):
        return f'{self.url_name}'

    def get_absolute_url(self):
        return reverse('ranking', args=[str(self.url_name)])

    pass


class Game(models.Model):
    game = models.CharField(max_length=50, help_text="Enter a game name", validators=[alpha_numeric], primary_key=True)

    def __str__(self):
        return f'{self.game}'

    pass


class Format(models.Model):
    format = models.CharField(max_length=50, help_text="Enter a format name for the game", validators=[alpha_numeric])
    game = models.ManyToManyField(Game, through='GameAndFormatMeta')

    def __str__(self):
        return f'{self.format}'

    pass


class GameAndFormatMeta(models.Model):
    organiser = models.ForeignKey(RankSite, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)

    number_of_tournaments_to_be_counted = models.IntegerField(default=30)
    max_time_back = models.IntegerField(default=365)

    class Meta:
        ordering = ['organiser', 'game', 'format']
        unique_together = ('organiser', 'game', 'format')

    def __str__(self):
        return f'{self.game} - {self.format}'

    pass


class Tournament(models.Model):
    date = models.DateField()
    game_and_format = models.ForeignKey(GameAndFormatMeta, on_delete=models.CASCADE,
                                        help_text="Format of the Tournament (e.g. Standard, Modern, ...)")
    points_per_win = models.IntegerField(default=2)
    points_per_draw = models.IntegerField(default=1)
    minus_points_per_loss = models.IntegerField(default=0)
    points_for_attendance = models.IntegerField(default=3)
    points_for_rank_one = models.IntegerField(default=3)

    class Meta:
        ordering = ['date', 'game_and_format']

    def __str__(self):
        return f'{self.date}, {self.game_and_format}'

    pass


class Player(models.Model):
    # ranker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
    #                              help_text="Unique Id accross whole website")
    # maybe in the future a score and avg rank for every player, that gets only updated,
    # when an official store uploads data - and gets then shown everywhere as the score

    organiser = models.ForeignKey(RankSite, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    game_id = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name', 'game_id', 'organiser']
        unique_together = ('last_name', 'first_name', 'game_id', 'organiser')

    def __str__(self):
        return f'{self.last_name}, {self.first_name}, {self.game_id}'

    pass


class Score(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    class Meta:
        ordering = ['tournament', 'wins', 'draws', 'losses', 'player']

    def __str__(self):
        return f'{self.tournament}, {self.player}, ({self.wins}, {self.losses}, {self.draws})'

    pass


class CurrentScore(models.Model):
    organiser = models.ForeignKey(RankSite, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    current_score = models.IntegerField(default=0)

    class Meta:
        ordering = ['organiser', 'game', 'format', 'player', 'current_score']

    def __str__(self):
        return f'{self.organiser}, {self.game}, {self.format}, {self.player}, {self.current_score}'

    pass
