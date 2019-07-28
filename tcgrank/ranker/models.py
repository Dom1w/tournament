from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class RankSite(models.Model):
    site_user = models.OneToOneField(User, on_delete=models.CASCADE)
    url_name = models.CharField(max_length=50, help_text="Enter a name for you sub-url of tcgrank", primary_key=True)

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
        """String for representing the Model object."""
        return f'{self.url_name}'

    pass


class Tournament(models.Model):
    organiser = models.ForeignKey(RankSite, on_delete=models.CASCADE)
    date = models.DateField()
    format = models.CharField(max_length=20, help_text="Format of the Tournament (e.g. Standard, Modern, ...)")
    points_per_win = models.IntegerField(default=2)
    points_per_draw = models.IntegerField(default=1)
    minus_points_per_loss = models.IntegerField(default=1)
    points_for_attendance = models.IntegerField(default=3)
    points_for_rank_one = models.IntegerField(default=3)
    pass


class Score(models.Model):
    pass


class Player(models.Model):
    pass
