from django.urls import path
from . import views


app_name = 'season'

urlpatterns = [
    path('', views.SeasonListView.as_view(), name='season_list'),
    path('bat-dau/', views.SeasonCreateView.as_view(), name='season_create'),
    path('<slug:slug>/', views.SeasonDetailView.as_view(), name='season_detail'),
]
