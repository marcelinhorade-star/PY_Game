import pygame

# Distância máxima (em pixels) que o tiro anda antes de sumir.
ALCANCE = 800


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
        self.distancia = 0  # quanto o tiro já andou

    def update(self):
        """Move o tiro e apaga quando ele passa do alcance.

        Usa a distância percorrida, e não a posição na tela, porque com a
        câmera as posições são do mapa inteiro (que é maior que a tela).
        """
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.distancia += abs(self.vel_x) + abs(self.vel_y)
        if self.distancia > ALCANCE:
            self.kill()