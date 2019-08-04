from django.contrib import admin

from ranker.models import RankSite, Tournament, Player, Score, GameFormatCombination, CurrentScore, Game, Format
# Register your models here.

admin.site.register(RankSite)
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Score)
admin.site.register(GameFormatCombination)
admin.site.register(CurrentScore)
admin.site.register(Game)
admin.site.register(Format)
