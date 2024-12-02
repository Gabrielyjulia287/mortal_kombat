from django.contrib import admin
from django.urls import path
from app import views  # Importando as views do app

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.login_view, name='login'),  # A URL inicial vai para o login
    path('index/', views.index, name='index'),  # Página de índice, será acessada após o login
     path('register/', views.register, name='register'),  # URL para a página de registro
    path('play/', views.play_game, name='play_game'),  # Corrigido o nome da rota
    path('ranking/', views.ranking_view, name='ranking'),
    path('signup/', views.signup_view, name='signup'), 
]
