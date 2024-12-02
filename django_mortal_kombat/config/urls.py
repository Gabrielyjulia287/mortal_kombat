from django.contrib import admin
from django.urls import path
from app import views  # Importando as views do app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # URL para a página inicial
    path('login/', views.login_view, name='login'),
    path('play/', views.play_game, name='play_game'),  # Corrigido o nome da rota
    path('ranking/', views.ranking_view, name='ranking'),
    path('signup/', views.signup_view, name='signup'), 
]
