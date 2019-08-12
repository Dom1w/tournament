from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from tcgrank import settings

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'triangle.svg')),

    path('mysite/', views.FormatInGameInstanceListView.as_view(), name='mysite'),
    # path('gameandformat/<int:pk>/update/', views.GameFormatCombinationUpdateView.as_view(), name='game_format_change'),

    path('upload/', views.upload, name='upload'),
    path('futurework/', views.futurework, name='futurework'),
    path('register/', views.register, name='register'),

    path('<pk>', views.ranking, name='ranking'),
    path('<site_name>/<game>/<format>/', views.ranking_user_game_format, name='rank_game_format')
]

urlpatterns += [
    path('mysite/password/', views.change_password, name='change_password'),
]
# urlpatterns += [
#     path('subscribe/', views.subscribe),
# ]
#from ranker.views import how_account, future_work, about
