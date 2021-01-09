from django.urls import path
from . import views


urlpatterns = [
    path('seasons/', views.season_list, name='season_list'),
]
