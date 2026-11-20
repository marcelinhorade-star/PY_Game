import pygame


class Tiro(pygame.sprite.Sprite):
    """Projétil que anda em linha reta, na horizontal ou para cima."""

    def __init__(self, x, y, direcao, para_cima=False):
        """Cria o tiro em (x, y).

        direcao: 1 (direita) ou -1 (esquerda), usado no tiro horizontal.
        para_cima: se True, o tiro sobe em vez de andar para os lados.
        """
        super().__init__()
        if para_cima:
            self.image = pygame.Surface((4, 10))   # tiro em pé
            self.vel_x = 0
            self.vel_y = -12
        else:
            self.image = pygame.Surface((10, 4))   # tiro deitado
            self.vel_x = 12 * direcao
            self.vel_y = 0
        self.image.fill((255, 220, 0))  # amarelo
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """Move o tiro e apaga quando sai da tela."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0:
            self.kill()