import pygame

class Tiro(pygame.sprite.Sprite):
    """Projétil que anda em linha reta."""

    def __init__(self, x, y, direcao):
        """Cria o tiro em (x, y) indo para a direção dada (1 ou -1)."""
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 220, 0))  # amarelo
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 12 * direcao

    def update(self):
        """Move o tiro e apaga quando sai da tela."""
        self.rect.x += self.velocidade
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()