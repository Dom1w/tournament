from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('futurework/', views.futurework, name='futurework'),
    path('<pk>', views.ranking, name='ranking'),
]

# urlpatterns += [
#     path('subscribe/', views.subscribe),
# ]
#from ranker.views import how_account, future_work, about
