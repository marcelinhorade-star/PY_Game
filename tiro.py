import os
import pygame

# Distância máxima (em pixels) que o tiro anda antes de sumir.
ALCANCE = 800

# Imagem da bala (do pack "Generic RUN n' GUN", CC0).
# os.path.dirname(__file__) = pasta onde está este arquivo, então o caminho
# funciona não importa de qual pasta o jogo for rodado.
CAMINHO_BALA = os.path.join(os.path.dirname(__file__), "imagens", "tiro", "bala.png")

# Clarão que aparece na ponta da arma a cada tiro (do mesmo pack).
CAMINHO_CLARAO = os.path.join(os.path.dirname(__file__), "imagens", "tiro", "clarao.png")

# Quanto tempo (ms) o clarão fica na tela.
DURACAO_CLARAO = 70

# As imagens originais são pequenas; aumentamos igual ao jogador.
ESCALA = 2

# Guardam as imagens depois da primeira vez, para não ler o arquivo a cada tiro.
_imagem_bala = None
_imagem_clarao = None


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


def carregar_imagem_clarao():
    """Devolve a imagem do clarão virada para a direita (ou None se não existir)."""
    global _imagem_clarao
    if _imagem_clarao is None and os.path.isfile(CAMINHO_CLARAO):
        imagem = pygame.image.load(CAMINHO_CLARAO).convert_alpha()
        _imagem_clarao = pygame.transform.scale_by(imagem, ESCALA)
    return _imagem_clarao


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


class Clarao(pygame.sprite.Sprite):
    """Clarão rápido na ponta da arma, que some depois de DURACAO_CLARAO ms.

    Fica no mesmo grupo dos tiros (para ser desenhado junto), mas não é um
    tiro: o rect dele tem tamanho 0, então nunca colide com nada.
    """

    def __init__(self, jogador):
        """Cria o clarão grudado na arma do jogador."""
        super().__init__()
        self.jogador = jogador
        self.criado_em = pygame.time.get_ticks()
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)  # trocada no update
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update()

    def update(self):
        """Segue a ponta da arma (o jogador pode andar) e some quando o tempo acaba."""
        if pygame.time.get_ticks() - self.criado_em > DURACAO_CLARAO:
            self.kill()
            return
        x, y, para_cima = self.jogador.ponta_da_arma()
        direcao = self.jogador.direcao
        clarao = carregar_imagem_clarao()
        if clarao is None:
            # Plano B: um círculo amarelo desenhado na hora.
            clarao = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(clarao, (255, 240, 120), (5, 5), 5)

        # Gira/vira a imagem e acha o canto de cima à esquerda (x0, y0)
        # para que a base do clarão fique encostada na ponta da arma.
        if para_cima:
            self.image = pygame.transform.rotate(clarao, 90)
            x0 = x - self.image.get_width() // 2
            y0 = y - self.image.get_height()
        elif direcao == -1:
            self.image = pygame.transform.flip(clarao, True, False)
            x0 = x - self.image.get_width()
            y0 = y - self.image.get_height() // 2
        else:
            self.image = clarao
            x0 = x
            y0 = y - self.image.get_height() // 2

        # Tamanho 0: a câmera desenha a imagem a partir deste canto, mas
        # colliderect/groupcollide nunca acham colisão com um rect vazio.
        self.rect = pygame.Rect(x0, y0, 0, 0)
