import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurações da Janela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Luta com Tiros")

# Ajustar tamanho das imagens
TAMANHO_PERSONAGEM = (100, 200)
TAMANHO_FUNDO = (LARGURA, ALTURA)

# Carregar e redimensionar imagens dos personagens
player1_img = pygame.image.load('player1.png')
player1_img = pygame.transform.scale(player1_img, TAMANHO_PERSONAGEM)

player2_img = pygame.image.load('player2.png')
player2_img = pygame.transform.scale(player2_img, TAMANHO_PERSONAGEM)

# Carregar imagem do fundo
fundo_img = pygame.image.load('fundo.png')
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

# Fontes
fonte = pygame.font.SysFont('arial', 30)

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
        # Dano de área (afeta todos os inimigos próximos)
        for outro in outros:
            if abs(self.x - outro.x) < 150 and abs(self.y - outro.y) < 150:
                outro.vida -= 10

    def teletransportar(self):
        self.x = random.randint(0, LARGURA - TAMANHO_PERSONAGEM[0])
        self.y = random.randint(0, ALTURA - TAMANHO_PERSONAGEM[1])

    def atualizar(self):
        # Desativar escudo após 5 segundos
        if self.escudo_ativo and pygame.time.get_ticks() - self.tempo_escudo > 5000:
            self.escudo_ativo = False

# Função principal do jogo
def jogo(player1, player2):
    round_atual = 1
    player1_vitorias = 0
    player2_vitorias = 0

    while player1_vitorias < 3 and player2_vitorias < 3:
        exibir_round(round_atual)
        player1.vida = 500
        player2.vida = 500
        exibir_go()

        tiros_destravados = False
        while player1.vida > 0 and player2.vida > 0:
            RELOGIO.tick(FPS)
            TELA.fill(BRANCO)
            TELA.blit(fundo_img, (0, 0))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            teclas = pygame.key.get_pressed()
            player1.mover(teclas, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
            player2.mover(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

            if teclas[pygame.K_SPACE]:
                player1.atirar(1, super_tiro=True)  # Super Tiro

            if teclas[pygame.K_KP0]:
                player2.atirar(-1, super_tiro=True)

            if teclas[pygame.K_c]:  # Ativar escudo para player1
                player1.ativar_escudo()

            if teclas[pygame.K_v]:  # Ativar ataque de área para player1
                player1.ativar_ataque_area([player2])

            if teclas[pygame.K_t]:  # Teletransporte para player1
                player1.teletransportar()

            player1.atualizar_projeteis(player2)
            player2.atualizar_projeteis(player1)

            player1.atualizar()
            player2.atualizar()

            player1.desenhar()
            player2.desenhar()

            for proj in player1.projeteis + player2.projeteis:
                proj.desenhar()

            pygame.display.flip()

        if player1.vida > 0:
            player1_vitorias += 1
        else:
            player2_vitorias += 1

        round_atual += 1

    exibir_vencedor(player1_vitorias, player2_vitorias)

# Funções para exibir tela de menu, round e vencedor
def desenhar_menu():
    TELA.fill(BRANCO)
    titulo = fonte.render("Jogo de Luta - Pressione Enter para Jogar", True, PRETO)
    TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2))
    pygame.display.flip()

def exibir_round(round_num):
    TELA.fill(BRANCO)
    titulo = fonte.render(f"Round {round_num}", True, PRETO)
    TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def exibir_go():
    TELA.fill(BRANCO)
    go_msg = fonte.render("GO!", True, PRETO)
    TELA.blit(go_msg, (LARGURA // 2 - go_msg.get_width() // 2, ALTURA // 2))
    pygame.display.flip()
    pygame.time.delay(1000)

def exibir_vencedor(player1_vitorias, player2_vitorias):
    TELA.fill(BRANCO)
    vencedor = "Player 1" if player1_vitorias == 3 else "Player 2"
    msg = fonte.render(f"{vencedor} é o campeão!", True, VERMELHO)
    TELA.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

player1 = Personagem(100, 300, player1_img, AZUL)
player2 = Personagem(600, 300, player2_img, VERMELHO)

while True:
    desenhar_menu()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            jogo(player1, player2)
