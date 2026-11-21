"""Cenário das fases: plataformas, inimigos, comprimento do mapa e fim da fase."""
import pygame
from inimigo import Inimigo, Drone, carregar_assets_inimigos

COR_TERRA = (100, 70, 45)

# Qual classe cria cada tipo de inimigo escrito na lista da fase.
TIPOS_INIMIGOS = {"soldado": Inimigo, "drone": Drone}

# Cada fase é um dicionário. Tudo em coordenadas do MUNDO (o mapa inteiro):
# plataformas são (x, y, largura, altura) e inimigos são (tipo, x, y dos pés).
FASES = [
    {
        "comprimento": 3000,
        "cor_ceu": (110, 170, 220),
        "plataformas": [
            (0, 550, 3000, 50),     # chão
            (400, 450, 150, 20),
            (650, 400, 150, 20),
            (1100, 450, 200, 20),
            (1500, 420, 120, 20),
            (1700, 360, 160, 20),
            (2200, 450, 200, 20),
        ],
        "inimigos": [
            ("soldado", 900, 550),
            ("soldado", 725, 400),
            ("drone", 1400, 300),
            ("soldado", 1780, 360),
            ("soldado", 2000, 550),
            ("drone", 2500, 280),
            ("soldado", 2700, 550),
        ],
    },
    {
        "comprimento": 3600,
        "cor_ceu": (230, 150, 100),
        "plataformas": [
            (0, 550, 3600, 50),     # chão
            (300, 460, 120, 20),
            (500, 390, 120, 20),
            (750, 450, 200, 20),
            (1050, 400, 150, 20),
            (1300, 340, 150, 20),
            (1600, 450, 250, 20),
            (2000, 420, 150, 20),
            (2250, 360, 150, 20),
            (2500, 300, 150, 20),
            (2900, 450, 300, 20),
        ],
        "inimigos": [
            ("soldado", 600, 550),
            ("soldado", 850, 450),
            ("drone", 1100, 280),
            ("soldado", 1375, 340),
            ("drone", 1700, 300),
            ("soldado", 1725, 450),
            ("soldado", 2075, 420),
            ("drone", 2400, 250),
            ("soldado", 2575, 300),
            ("drone", 3000, 300),
            ("soldado", 3050, 450),
            ("soldado", 3300, 550),
        ],
    },
]


class Plataforma(pygame.sprite.Sprite):
    """Retângulo sólido onde o jogador e os inimigos podem ficar em cima."""

    def __init__(self, x, y, largura, altura):
        """Cria a plataforma com o canto superior esquerdo em (x, y)."""
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(COR_TERRA)
        self.rect = self.image.get_rect(topleft=(x, y))


class Fase:
    """Monta o cenário de uma fase a partir da lista FASES e cuida dos inimigos."""

    def __init__(self, numero):
        """Cria a fase de índice numero (0 = primeira fase)."""
        dados = FASES[numero]
        self.numero = numero
        self.comprimento = dados["comprimento"]
        self.cor_ceu = dados["cor_ceu"]

        self.plataformas = pygame.sprite.Group()
        for x, y, largura, altura in dados["plataformas"]:
            self.plataformas.add(Plataforma(x, y, largura, altura))

        self.inimigos = pygame.sprite.Group()
        self.tiros_inimigos = pygame.sprite.Group()
        self.efeitos = pygame.sprite.Group()
        grupos = {"tiros_inimigos": self.tiros_inimigos, "efeitos": self.efeitos}
        assets = carregar_assets_inimigos()   # imagens carregadas uma vez só
        for tipo, x, y in dados["inimigos"]:
            classe = TIPOS_INIMIGOS[tipo]
            self.inimigos.add(classe(x, y, assets, grupos))

    def atualizar(self, jogador):
        """Atualiza inimigos, tiros inimigos e explosões (uma vez por quadro)."""
        self.inimigos.update(jogador, self.plataformas)
        self.tiros_inimigos.update()
        self.efeitos.update()

    def desenhar(self, tela, camera):
        """Desenha o céu e tudo da fase, deslocado pela câmera."""
        tela.fill(self.cor_ceu)
        camera.desenhar_grupo(tela, self.plataformas)
        camera.desenhar_grupo(tela, self.inimigos)
        camera.desenhar_grupo(tela, self.tiros_inimigos)
        camera.desenhar_grupo(tela, self.efeitos)

    def terminou(self, jogador):
        """Retorna True quando o jogador chega ao fim do mapa."""
        return jogador.rect.right >= self.comprimento


def existe_fase(numero):
    """Retorna True se existe uma fase com esse índice (para saber se o jogo acabou)."""
    return numero < len(FASES)
