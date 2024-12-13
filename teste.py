import pygame
import random
from pygame.locals import *

# Cores
branco = (255, 255, 255)
preto = (254,161,182)
azul = (0, 0, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
cores_objetos = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (188, 11, 243)]
rosa= ((192,217,217 ))
# Dimensões da tela
largura_tela = 600
altura_tela = 600

# Inicializar Pygame e Música
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("musica_jogo.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

screen = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Jogo da Cobrinha')

# Direções
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Função para gerar posição aleatória na grade
def on_grid_random():
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return x * 10, y * 10

# Função para verificar colisão
def colisao(c1, c2):
    return c1 == c2

# Classe para a cobra
class Cobra:
    def __init__(self):
        self.corpo = [(200, 200), (210, 200), (220, 200), (230, 200)]
        self.cor = branco
        self.direcao = LEFT

    def mover(self):
        x = self.corpo[0][0]
        y = self.corpo[0][1]

        if self.direcao == UP:
            y -= 10
        elif self.direcao == DOWN:
            y += 10
        elif self.direcao == RIGHT:
            x += 10
        elif self.direcao == LEFT:
            x -= 10

        self.corpo.insert(0, (x, y))
        self.corpo.pop()

    def desenhar(self):
        for pos in self.corpo:
            pygame.draw.rect(screen, self.cor, pygame.Rect(pos[0], pos[1], 10, 10))

    # Função para verificar colisão com as bordas
    def colidir_com_borda(self):
        x, y = self.corpo[0]
        return x < 0 or x >= largura_tela or y < 0 or y >= altura_tela

# Classe para o objeto (frutinha)
class Objeto:
    def __init__(self):
        self.pos = on_grid_random()
        self.cor = random.choice(cores_objetos)

    def desenhar(self):
        pygame.draw.rect(screen, self.cor, pygame.Rect(self.pos[0], self.pos[1], 10, 10))

# Função para desenhar botões
def desenhar_botao(texto, x, y, largura, altura, cor_texto, cor_fundo):
    pygame.draw.rect(screen, cor_fundo, (x, y, largura, altura))
    font = pygame.font.Font(None, 36)
    text = font.render(texto, True, cor_texto)
    text_rect = text.get_rect(center=(x + largura // 2, y + altura // 2))
    screen.blit(text, text_rect)

# Função para desenhar textos
def desenhar_texto(texto, tamanho, x, y, cor):
    font = pygame.font.Font(None, tamanho)
    text = font.render(texto, True, cor)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

# Inicialização
cobra = Cobra()
objeto = Objeto()
clock = pygame.time.Clock()
placar = 0
font = pygame.font.Font(None, 36)

# Estados do jogo
TELA_START = 0
TELA_JOGO = 1
TELA_GAME_OVER = 2
TELA_PLACAR = 3
TELA_OPCOES = 4
estado_jogo = TELA_START

# Definir botões
botao_x = largura_tela // 2 - 100
botao_y = altura_tela // 2
largura_botao = 200
altura_botao = 50

# Loop principal do jogo
running = True
while running:
    screen.fill(preto)

    if estado_jogo == TELA_START:
        desenhar_texto("Bem-vindo ao Jogo da Cobrinha", 36, largura_tela // 2, altura_tela // 2 - 100, branco)
        desenhar_botao("Iniciar Jogo", botao_x, botao_y, largura_botao, altura_botao, branco, rosa)
        desenhar_botao("Placar", botao_x, botao_y + 60, largura_botao, altura_botao, branco, rosa)
        desenhar_botao("Opções", botao_x, botao_y + 120, largura_botao, altura_botao, branco, rosa)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if botao_x <= x <= botao_x + largura_botao and botao_y <= y <= botao_y + altura_botao:
                    estado_jogo = TELA_JOGO
                elif botao_x <= x <= botao_x + largura_botao and botao_y + 60 <= y <= botao_y + 60 + altura_botao:
                    estado_jogo = TELA_PLACAR
                elif botao_x <= x <= botao_x + largura_botao and botao_y + 120 <= y <= botao_y + 120 + altura_botao:
                    estado_jogo = TELA_OPCOES

    elif estado_jogo == TELA_JOGO:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP and cobra.direcao != DOWN:
                    cobra.direcao = UP
                elif event.key == K_DOWN and cobra.direcao != UP:
                    cobra.direcao = DOWN
                elif event.key == K_RIGHT and cobra.direcao != LEFT:
                    cobra.direcao = RIGHT
                elif event.key == K_LEFT and cobra.direcao != RIGHT:
                    cobra.direcao = LEFT

        # Move a cobra
        cobra.mover()

        # Verifica colisão com a frutinha
        if colisao(cobra.corpo[0], objeto.pos):
            cobra.cor = objeto.cor
            objeto.pos = on_grid_random()
            objeto.cor = random.choice(cores_objetos)
            cobra.corpo.append((0, 0))
            placar += 1

        # Verifica colisão com as bordas
        if cobra.colidir_com_borda():
            estado_jogo = TELA_GAME_OVER

        cobra.desenhar()
        objeto.desenhar()
        score_text = font.render("Score: " + str(placar), True, branco)
        screen.blit(score_text, [10, 10])

    elif estado_jogo == TELA_GAME_OVER:
        screen.fill(preto)
        desenhar_texto("Game Over", 48, largura_tela // 2, altura_tela // 2 - 50, vermelho)
        desenhar_botao("Reiniciar", botao_x, botao_y, largura_botao, altura_botao, branco, verde)
        desenhar_botao("Menu", botao_x, botao_y + 60, largura_botao, altura_botao, branco, azul)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if botao_x <= x <= botao_x + largura_botao and botao_y <= y <= botao_y + altura_botao:
                    cobra = Cobra()
                    objeto = Objeto()
                    placar = 0
                    estado_jogo = TELA_JOGO
                elif botao_x <= x <= botao_x + largura_botao and botao_y + 60 <= y <= botao_y + 60 + altura_botao:
                    estado_jogo = TELA_START

    pygame.display.update()
    clock.tick(10)

pygame.quit()
