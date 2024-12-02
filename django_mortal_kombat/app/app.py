import os
import django
from flask import Flask, render_template, redirect, url_for
from django.contrib.auth.models import User
from .models import Pontuacao
from jogo import jogo, Personagem  # importando o seu código do jogo
import pygame

# Definir a variável de ambiente DJANGO_SETTINGS_MODULE para o seu projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_mortal_kombat.settings')

# Inicializar o Django
django.setup()

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para jogar o jogo
@app.route('/play')
def play_game():
    # Substitua com a lógica para pegar o usuário autenticado
    try:
        usuario_atual = User.objects.get(username="user_example")  # Ajuste conforme sua lógica de autenticação
    except User.DoesNotExist:
        return redirect(url_for('index'))

    # Criando os personagens
    player1 = Personagem(100, 300, 'player1.png', (0, 0, 255))
    player2 = Personagem(600, 300, 'player2.png', (255, 0, 0))
    
    # Iniciar o jogo
    jogo(player1, player2, usuario_atual)  # Iniciar o jogo Pygame (certifique-se de que a função `jogo` lida com a lógica corretamente)

    # Após o jogo, redirecionar para a página de ranking
    return redirect(url_for('ranking'))

# Rota para mostrar o ranking
@app.route('/ranking')
def ranking():
    # Exibindo os 10 melhores rankings, por exemplo
    rankings = Pontuacao.objects.all().order_by('-pontuacao')[:10]
    return render_template('ranking.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True)
