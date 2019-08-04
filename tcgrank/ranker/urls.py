from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('mysite/', views.FormatInGameInstanceListView.as_view(), name='mysite'),
    # path('gameandformat/<int:pk>/update/', views.GameFormatCombinationUpdateView.as_view(), name='game_format_change'),


    path('upload/', views.upload, name='upload'),
    path('futurework/', views.futurework, name='futurework'),
    path('register/', views.register, name='register'),
    path('<pk>', views.ranking, name='ranking'),
]

urlpatterns += [
    path('mysite/password/', views.change_password, name='change_password'),
]
# urlpatterns += [
#     path('subscribe/', views.subscribe),
# ]
#from ranker.views import how_account, future_work, about
