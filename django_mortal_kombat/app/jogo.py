import pygame
import sys
import random
import os
from .models import Pontuacao
from django.contrib.auth.models import User

# Inicialize o Pygame
pygame.init()

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretórios das imagens (ajustar conforme sua estrutura de pastas)
IMAGEM_PLAYER1 = os.path.join(BASE_DIR, 'static', 'images', 'player1.png')
IMAGEM_PLAYER2 = os.path.join(BASE_DIR, 'static', 'images', 'player2.png')
IMAGEM_FUNDO = os.path.join(BASE_DIR, 'static', 'images', 'fundo.png')

# Configurações da Janela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Luta com Tiros")

# Ajustar tamanho das imagens
TAMANHO_PERSONAGEM = (100, 200)
TAMANHO_FUNDO = (LARGURA, ALTURA)

# Carregar e redimensionar imagens dos personagens
player1_img = pygame.image.load(IMAGEM_PLAYER1)
player1_img = pygame.transform.scale(player1_img, TAMANHO_PERSONAGEM)

player2_img = pygame.image.load(IMAGEM_PLAYER2)
player2_img = pygame.transform.scale(player2_img, TAMANHO_PERSONAGEM)

# Carregar imagem do fundo
fundo_img = pygame.image.load(IMAGEM_FUNDO)
fundo_img = pygame.transform.scale(fundo_img, TAMANHO_FUNDO)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# FPS (Frames por Segundo)
FPS = 60
RELOGIO = pygame.time.Clock()

# Fontes (Agora podemos carregar a fonte porque o Pygame foi inicializado)
fonte = pygame.font.SysFont('arial', 30)

# Função para salvar a pontuação no banco de dados
def salvar_pontuacao(usuario, ganhador):
    try:
        # Crie ou obtenha o usuário no banco de dados
        usuario = User.objects.get(username=usuario)
        # Registra a pontuação (substitua Pontuacao com o modelo do seu Django)
        Pontuacao.objects.create(usuario=usuario, ganhador=ganhador)
        print(f"Pontuação de {ganhador} salva com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar a pontuação no banco de dados: {e}")

# Função para sair do jogo
def sair_do_jogo():
    pygame.quit()
    

# Classe Projétil
class Projetil:
    def __init__(self, x, y, direcao, cor, dano=2):
        self.x = x
        self.y = y
        self.velocidade = 10 * direcao
        self.cor = cor
        self.raio = 5
        self.dano = dano

    def mover(self):
        self.x += self.velocidade

    def desenhar(self):
        pygame.draw.circle(TELA, self.cor, (self.x, self.y), self.raio)

    def fora_da_tela(self):
        return self.x < 0 or self.x > LARGURA

# Classe Personagem
class Personagem:
    def __init__(self, x, y, imagem, cor):
        self.x = x
        self.y = y
        self.imagem = imagem
        self.rect = self.imagem.get_rect(topleft=(x, y))
        self.vida = 500
        self.velocidade = 5
        self.cor = cor
        self.projeteis = []
        self.escudo_ativo = False
        self.tempo_escudo = 0
        self.poder_ativo = False

    def desenhar(self):
        TELA.blit(self.imagem, (self.x, self.y))
        pygame.draw.rect(TELA, PRETO, (self.x, self.y - 20, 200, 10))
        vida_percentual = (self.vida / 500) * 200
        pygame.draw.rect(TELA, self.cor, (self.x, self.y - 20, vida_percentual, 10))

    def mover(self, teclas, esquerda, direita, cima, baixo):
        if teclas[esquerda] and self.x > 0:
            self.x -= self.velocidade
        if teclas[direita] and self.x < LARGURA - TAMANHO_PERSONAGEM[0]:
            self.x += self.velocidade
        if teclas[cima] and self.y > 0:
            self.y -= self.velocidade
        if teclas[baixo] and self.y < ALTURA - TAMANHO_PERSONAGEM[1]:
            self.y += self.velocidade
        self.rect.topleft = (self.x, self.y)

    def atirar(self, direcao, super_tiro=False):
        dano = 5 if super_tiro else 2  # Super tiro causa mais dano
        novo_projetil = Projetil(
            self.x + TAMANHO_PERSONAGEM[0] // 2,
            self.y + TAMANHO_PERSONAGEM[1] // 2,
            direcao,
            self.cor,
            dano
        )
        self.projeteis.append(novo_projetil)

    def atualizar_projeteis(self, outro):
        for proj in self.projeteis[:]:
            proj.mover()
            if proj.fora_da_tela():
                self.projeteis.remove(proj)
            elif (
                proj.x - proj.raio < outro.rect.right and
                proj.x + proj.raio > outro.rect.left and
                proj.y > outro.rect.top and
                proj.y < outro.rect.bottom
            ):
                if not outro.escudo_ativo:  # Se não tiver escudo, aplicar dano
                    outro.vida -= proj.dano
                self.projeteis.remove(proj)

    def ativar_escudo(self):
        self.escudo_ativo = True
        self.tempo_escudo = pygame.time.get_ticks()

    def ativar_ataque_area(self, outros):
        for outro in outros:
            if abs(self.x - outro.x) < 150 and abs(self.y - outro.y) < 150:
                outro.vida -= 10

    def teletransportar(self):
        self.x = random.randint(0, LARGURA - TAMANHO_PERSONAGEM[0])
        self.y = random.randint(0, ALTURA - TAMANHO_PERSONAGEM[1])

    def atualizar(self):
        if self.escudo_ativo and pygame.time.get_ticks() - self.tempo_escudo > 5000:
            self.escudo_ativo = False

# Função para exibir o início do round
def exibir_round(round_atual):
    texto = fonte.render(f"Round {round_atual}", True, AZUL)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(1000)


# Função para exibir a tela de vencedor com opções de reiniciar ou sair
def exibir_vencedor(player1_vitorias, player2_vitorias):
    vencedor = "Jogador 1" if player1_vitorias > player2_vitorias else "Jogador 2"
    texto = fonte.render(f"{vencedor} é o vencedor!", True, VERDE)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
    
    # Exibir opções de jogar novamente ou sair
    texto_opcoes = fonte.render("Pressione R para jogar novamente ou Q para sair", True, AZUL)
    TELA.blit(texto_opcoes, (LARGURA // 2 - texto_opcoes.get_width() // 2, ALTURA // 2 + 40))

    pygame.display.flip()

    # Aguardar a tecla pressionada (R para reiniciar ou Q para sair)
    continuar_jogo = True
    while continuar_jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair_do_jogo()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:  # Tecla Q para sair
                    sair_do_jogo()
                elif evento.key == pygame.K_r:  # Tecla R para reiniciar o jogo
                    return True  # Retorna True para reiniciar o jogo
        RELOGIO.tick(FPS)

# Função principal do jogo
def jogo(player1, player2, usuario):
    round_atual = 1
    player1_vitorias = 0
    player2_vitorias = 0

    while player1_vitorias < 3 and player2_vitorias < 3:
        exibir_round(round_atual)

        # Reinicia a vida dos jogadores no início de cada round
        player1.vida = 500
        player2.vida = 500

        # Loop do round
        while player1.vida > 0 and player2.vida > 0:
            RELOGIO.tick(FPS)
            TELA.fill(BRANCO)
            TELA.blit(fundo_img, (0, 0))

            # Eventos do jogo
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sair_do_jogo()

            # Movimentação e ações dos jogadores
            teclas = pygame.key.get_pressed()
            player1.mover(teclas, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
            player2.mover(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

            if teclas[pygame.K_SPACE]:
                player1.atirar(1, super_tiro=True)

            if teclas[pygame.K_KP0]:
                player2.atirar(-1, super_tiro=True)

            if teclas[pygame.K_c]:  # Ativar escudo para player1
                player1.ativar_escudo()

            if teclas[pygame.K_v]:  # Ativar ataque de área para player1
                player1.ativar_ataque_area([player2])

            if teclas[pygame.K_t]:  # Teletransporte para player1
                player1.teletransportar()

            # Atualização dos projéteis e status dos jogadores
            player1.atualizar_projeteis(player2)
            player2.atualizar_projeteis(player1)

            player1.atualizar()
            player2.atualizar()

            # Desenhar na tela
            player1.desenhar()
            player2.desenhar()

            for proj in player1.projeteis + player2.projeteis:
                proj.desenhar()

            pygame.display.flip()

        # Registrar quem venceu o round
        if player1.vida > 0:
            player1_vitorias += 1
            print(f"Jogador Vermelho venceu o round! Vitórias: {player1_vitorias}")
        else:
            player2_vitorias += 1
            print(f"Jogador Azul venceu o round! Vitórias: {player2_vitorias}")

        round_atual += 1

    # Determinar o vencedor final
    ganhador = 'vermelho' if player1_vitorias > player2_vitorias else 'azul'

    # Log do vencedor
    print(f"Jogo finalizado! Vencedor: {ganhador} - Player 1 Vitórias: {player1_vitorias}, Player 2 Vitórias: {player2_vitorias}")

    # Salvar a pontuação no banco de dados
    salvar_pontuacao(usuario, ganhador)

    # Exibir o vencedor na tela
    if exibir_vencedor(player1_vitorias, player2_vitorias):
        jogo(player1, player2, usuario)  # Reinicia o jogo se o jogador pressionar "R"
    else:
        sair_do_jogo()  # Sai se o jogador pressionar "Q"

    # Retorna o vencedor para controle externo
    return ganhador

# Iniciar o jogo com os jogadores
player1 = Personagem(100, ALTURA // 2, player1_img, VERMELHO)
player2 = Personagem(LARGURA - 200, ALTURA // 2, player2_img, AZUL)
