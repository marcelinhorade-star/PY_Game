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
        self.ultimo_dano = -10000   # NOVO: momento (ms) do último dano
        self.invencivel_ms = 1000   # NOVO: tempo de invencibilidade após dano

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

    def esta_invencivel(self):
        """NOVO: retorna True se o jogador levou dano há pouco tempo."""
        return pygame.time.get_ticks() - self.ultimo_dano < self.invencivel_ms

    def levar_dano(self, quantidade=1):
        """NOVO: tira vida do jogador, se ele não estiver invencível.

        Retorna True se o dano foi aplicado, False se foi ignorado.
        """
        if self.esta_invencivel():
            return False
        self.vida -= quantidade
        if self.vida < 0:
            self.vida = 0
        self.ultimo_dano = pygame.time.get_ticks()
        return True

    def esta_vivo(self):
        """NOVO: retorna True enquanto o jogador tiver vida."""
        return self.vida > 0

    def piscar(self):
        """NOVO: faz o jogador piscar enquanto está invencível."""
        if self.esta_invencivel():
            visivel = (pygame.time.get_ticks() // 100) % 2 == 0
            self.image.set_alpha(255 if visivel else 80)
        else:
            self.image.set_alpha(255)

    def update(self, teclas, chao_y):
        """Atualiza o jogador a cada quadro."""
        self.mover(teclas)
        self.aplicar_gravidade(chao_y)
        self.piscar()  # NOVO