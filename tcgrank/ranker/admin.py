from django.contrib import admin

from ranker.models import RankSite, Tournament, Player, Score, FormatInGameInstance, CurrentScore, Game, FormatInGame
# Register your models here.

admin.site.register(RankSite)
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Score)
admin.site.register(FormatInGameInstance)
admin.site.register(CurrentScore)
admin.site.register(Game)


@admin.register(FormatInGame)
class FormatInGameAdmin(admin.ModelAdmin):
    list_display = ('game', 'format')
    #inlines = [BooksInstanceInline]