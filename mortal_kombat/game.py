import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurações da Janela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Luta com Tiros")

# Ajustar tamanho das imagens (Ex: 100x100 para personagens)
TAMANHO_PERSONAGEM = (100, 200)
TAMANHO_FUNDO = (LARGURA, ALTURA)

# Carregar e redimensionar imagens dos personagens
player1_img = pygame.image.load('player1.png')
player1_img = pygame.transform.scale(player1_img, TAMANHO_PERSONAGEM)

player2_img = pygame.image.load('player2.png')
player2_img = pygame.transform.scale(player2_img, TAMANHO_PERSONAGEM)

# Carregar imagem do fundo (uma única imagem)
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
    def __init__(self, x, y, direcao, cor):
        self.x = x
        self.y = y
        self.velocidade = 10 * direcao
        self.cor = cor
        self.raio = 5

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
        self.vida = 500  # A vida começa com 900 para durar mais
        self.velocidade = 5
        self.cor = cor
        self.projeteis = []

    def desenhar(self):
        TELA.blit(self.imagem, (self.x, self.y))
        pygame.draw.rect(TELA, PRETO, (self.x, self.y - 20, 200, 10))  # Barra de vida mais larga
        vida_percentual = (self.vida / 500) * 200  # A barra de vida vai até 200 pixels
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

    def atirar(self, direcao):
        novo_projetil = Projetil(self.x + TAMANHO_PERSONAGEM[0] // 2, self.y + TAMANHO_PERSONAGEM[1] // 2, direcao, self.cor)
        self.projeteis.append(novo_projetil)

    def atualizar_projeteis(self, outro):
        for proj in self.projeteis[:]:
            proj.mover()
            if proj.fora_da_tela():
                self.projeteis.remove(proj)
            elif proj.x - proj.raio < outro.rect.right and proj.x + proj.raio > outro.rect.left and proj.y > outro.rect.top and proj.y < outro.rect.bottom:
                outro.vida -= 2  # Diminui o dano para garantir que a vida demora mais a acabar
                self.projeteis.remove(proj)

def desenhar_menu():
    TELA.fill(BRANCO)
    titulo = fonte.render("Jogo de Luta - Pressione Enter para Jogar", True, PRETO)
    TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2))
    # Adicionar mensagem verde alertando sobre o desbloqueio dos tiros
    alerta = fonte.render("Pressione ENTER para começar e destravar os tiros!", True, VERDE)
    TELA.blit(alerta, (LARGURA // 2 - alerta.get_width() // 2, ALTURA // 2 + 50))
    pygame.display.flip()

def exibir_round(round_num):
    TELA.fill(BRANCO)
    titulo = fonte.render(f"Round {round_num}", True, PRETO)
    TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Exibe o round por 2 segundos

def exibir_go():
    TELA.fill(BRANCO)
    go_msg = fonte.render("GO!", True, PRETO)
    TELA.blit(go_msg, (LARGURA // 2 - go_msg.get_width() // 2, ALTURA // 2))
    pygame.display.flip()
    pygame.time.delay(1000)  # Exibe "GO!" por 1 segundo

def jogo(player1, player2):
    round_atual = 1
    player1_vitorias = 0
    player2_vitorias = 0

    while player1_vitorias < 3 and player2_vitorias < 3:
        # Exibe o round atual antes de começar o jogo
        exibir_round(round_atual)
        
        # Reseta a vida a cada round
        player1.vida = 500
        player2.vida = 500

        # Exibe "GO!" antes de permitir que os jogadores atirem
        exibir_go()

        # Fase de jogo começa após o "GO!" ser exibido
        tiros_destravados = False
        while player1.vida > 0 and player2.vida > 0:
            RELOGIO.tick(FPS)
            TELA.fill(BRANCO)
            TELA.blit(fundo_img, (0, 0))  # Usando o fundo único

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            teclas = pygame.key.get_pressed()
            player1.mover(teclas, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
            player2.mover(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

            # Destrava os tiros após o "GO!"
            if not tiros_destravados:
                tiros_destravados = True  # Após o "GO!", os tiros estão destravados

            # Agora que os tiros estão destravados, eles podem atirar
            if tiros_destravados:
                if teclas[pygame.K_SPACE]:
                    player1.atirar(1)
                if teclas[pygame.K_KP0]:
                    player2.atirar(-1)

            player1.atualizar_projeteis(player2)
            player2.atualizar_projeteis(player1)

            player1.desenhar()
            player2.desenhar()

            for proj in player1.projeteis + player2.projeteis:
                proj.desenhar()

            pygame.display.flip()

        # Verificação de vencedor do round
        if player1.vida > 0:
            player1_vitorias += 1
        else:
            player2_vitorias += 1

        round_atual += 1

    exibir_vencedor(player1_vitorias, player2_vitorias)

def exibir_vencedor(player1_vitorias, player2_vitorias):
    TELA.fill(BRANCO)
    if player1_vitorias == 3:
        vencedor = "Player 1"
    else:
        vencedor = "Player 2"
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
