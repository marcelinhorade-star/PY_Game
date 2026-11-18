import pygame
from tiro import Tiro


class Jogador(pygame.sprite.Sprite):
    """Personagem controlado pelo jogador."""

    def __init__(self, x, y):
        """Cria o jogador na posição (x, y)."""
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 120, 255))  # retângulo azul por enquanto
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel_y = 0
        self.no_chao = True
        self.vida = 3
        self.direcao = 1  # 1 = direita, -1 = esquerda
        self.ultimo_tiro = 0

    def mover(self, teclas):
        """Anda para os lados com as setas."""
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
            self.direcao = -1
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
            self.direcao = 1

    def pular(self):
        """Pula se estiver no chão."""
        if self.no_chao:
            self.vel_y = -15
            self.no_chao = False

    def atirar(self, grupo_tiros):
        """Cria um tiro, com intervalo de 250 ms entre tiros."""
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > 250:
            tiro = Tiro(self.rect.centerx, self.rect.centery, self.direcao)
            grupo_tiros.add(tiro)
            self.ultimo_tiro = agora

    def aplicar_gravidade(self, chao_y):
        """Puxa o jogador para baixo até o chão."""
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self.vel_y = 0
            self.no_chao = True

    def update(self, teclas, chao_y):
        """Atualiza o jogador a cada quadro."""
        self.mover(teclas)
        self.aplicar_gravidade(chao_y)