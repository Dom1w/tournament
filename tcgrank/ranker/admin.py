from django.contrib import admin

from ranker.models import RankSite, Tournament, Player, Score, GameAndFormat, CurrentScores
# Register your models here.

admin.site.register(RankSite)
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Score)
admin.site.register(GameAndFormat)
admin.site.register(CurrentScores)
