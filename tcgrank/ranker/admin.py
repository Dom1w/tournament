from django.contrib import admin

from ranker.models import RankSite, Tournament, Player, Score, GameAndFormatMeta, CurrentScore, Game, Format
# Register your models here.

admin.site.register(RankSite)
admin.site.register(Game)
admin.site.register(Format)



# todo comment all this out down below
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Score)
admin.site.register(CurrentScore)

@admin.register(GameAndFormatMeta)
class GameAndFormatMetaAdmin(admin.ModelAdmin):
    list_display = ('organiser', 'game', 'format')
    #inlines = [BooksInstanceInline]