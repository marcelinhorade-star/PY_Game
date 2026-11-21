import os
import pygame

# Distância máxima (em pixels) que o tiro anda antes de sumir.
ALCANCE = 800

# Imagem da bala (do pack "Generic RUN n' GUN", CC0).
# os.path.dirname(__file__) = pasta onde está este arquivo, então o caminho
# funciona não importa de qual pasta o jogo for rodado.
CAMINHO_BALA = os.path.join(os.path.dirname(__file__), "imagens", "tiro", "bala.png")

# A bala original tem 7x3 pixels; aumentamos igual ao jogador.
ESCALA = 2

# Guarda a imagem depois da primeira vez, para não ler o arquivo a cada tiro.
_imagem_bala = None


def carregar_imagem_bala():
    """Devolve a imagem da bala virada para a direita.

    Carrega do disco só na primeira chamada e depois reaproveita.
    Se o arquivo não existir, devolve None (aí o tiro vira um retângulo).
    """
    global _imagem_bala
    if _imagem_bala is None and os.path.isfile(CAMINHO_BALA):
        imagem = pygame.image.load(CAMINHO_BALA).convert_alpha()
        _imagem_bala = pygame.transform.scale_by(imagem, ESCALA)
    return _imagem_bala


class Tiro(pygame.sprite.Sprite):
    """Projétil que anda em linha reta, na horizontal ou para cima."""

    def __init__(self, x, y, direcao, para_cima=False):
        """Cria o tiro em (x, y).

        direcao: 1 (direita) ou -1 (esquerda), usado no tiro horizontal.
        para_cima: se True, o tiro sobe em vez de andar para os lados.
        """
        super().__init__()
        if para_cima:
            self.vel_x = 0
            self.vel_y = -12
        else:
            self.vel_x = 12 * direcao
            self.vel_y = 0

        bala = carregar_imagem_bala()
        if bala is not None:
            if para_cima:
                # rotate gira no sentido anti-horário: 90 graus deixa a
                # bala, que aponta para a direita, apontando para cima.
                self.image = pygame.transform.rotate(bala, 90)
            elif direcao == -1:
                # flip(imagem, espelhar_x, espelhar_y): vira para a esquerda.
                self.image = pygame.transform.flip(bala, True, False)
            else:
                self.image = bala
        else:
            # Plano B: sem a imagem, usa o retângulo amarelo de antes.
            if para_cima:
                self.image = pygame.Surface((4, 10))   # tiro em pé
            else:
                self.image = pygame.Surface((10, 4))   # tiro deitado
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
