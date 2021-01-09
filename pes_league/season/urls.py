from django.urls import path
from . import views


app_name = 'season'

urlpatterns = [
    path('mua-giai/', views.SeasonListView.as_view(), name='season_list'),
    path('mua-giai/them-mua-giai/', views.SeasonCreateView.as_view(), name='season_create'),
    path('mua-giai/<slug:slug>/', views.SeasonDetailView.as_view(), name='season_detail'),
    path('doi-bong/', views.TeamListView.as_view(), name='team_list'),
    path('doi-bong/them-doi-bong/', views.TeamCreateView.as_view(), name='team_create'),
    path('doi-bong/<slug:slug>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('tran-dau/', views.GameListView.as_view(), name='game_list'),
    path('tran-dau/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
]
