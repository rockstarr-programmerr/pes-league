from django.urls import path
from . import views


app_name = 'season'

urlpatterns = [
    path('seasons/', views.SeasonListView.as_view(), name='season_list'),
    path('seasons/create/', views.SeasonCreateView.as_view(), name='season_create'),
    path('seasons/<int:pk>/', views.SeasonDetailView.as_view(), name='season_detail'),
]
