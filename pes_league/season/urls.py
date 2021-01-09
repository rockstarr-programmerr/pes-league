from django.urls import path
from . import views


app_name = 'season'

urlpatterns = [
    path('mua-giai/', views.SeasonListView.as_view(), name='season_list'),
    path('mua-giai/create/', views.SeasonCreateView.as_view(), name='season_create'),
    path('mua-giai/<slug:slug>/', views.SeasonDetailView.as_view(), name='season_detail'),
]
