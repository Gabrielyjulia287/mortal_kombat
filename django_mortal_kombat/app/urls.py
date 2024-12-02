from django.urls import path
from . import views

urlpatterns = [
    path('ranking/', views.Pontuacao, name='ranking'),
    path('play/', views.play_game, name='play_game'),
]
