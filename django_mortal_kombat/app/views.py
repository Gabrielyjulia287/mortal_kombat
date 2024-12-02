from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import pygame
from .models import Pontuacao
import random  # Isso é apenas para gerar pontuação aleatória para o exemplo

# Função de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/')  # Redireciona para a página inicial após login
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha ambos os campos.')
    
    return render(request, 'login.html')

# Página inicial

@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def play_game(request):
    from .jogo import Personagem, player1_img, player2_img, VERMELHO, AZUL, jogo
    from .models import Pontuacao  # Importar Pontuacao aqui dentro da função
    pygame.init()

    # Criação dos jogadores
    player1 = Personagem(100, 300, player1_img, VERMELHO)
    player2 = Personagem(600, 300, player2_img, AZUL)

    # Chama a função do jogo e passa o usuário logado
    ganhador = jogo(player1, player2, request.user)

    # Salva a pontuação no banco de dados após o jogo
    salvar_pontuacao(request.user, ganhador)

    return redirect('ranking')  # Redireciona para a página de ranking






# Página de ranking
@login_required
def ranking_view(request):
    rankings = Pontuacao.objects.all().order_by('-data')  # Ordena os usuários pela data da pontuação
    return render(request, 'ranking.html', {'rankings': rankings})

# Função de signup (cadastro de usuários)
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Pontuacao.objects.create(usuario=user)  # Cria uma pontuação padrão para o novo usuário
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')  # Redireciona para a página de login após o cadastro
        else:
            messages.error(request, 'Erro ao criar a conta. Verifique os campos e tente novamente.')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

# Função para salvar a pontuação no banco de dados
# Função para salvar a pontuação no banco de dados
def salvar_pontuacao(usuario, ganhador):
    try:
        assert ganhador in ['vermelho', 'azul'], f"Ganhador inválido: {ganhador}"
        Pontuacao.objects.create(usuario=usuario, ganhador=ganhador)
        print(f"Salvo: Usuario={usuario}, Ganhador={ganhador}")
    except AssertionError as ae:
        print(f"Erro de validação: {ae}")
    except Exception as e:
        print(f"Erro ao salvar a pontuação no banco de dados: {e}")





