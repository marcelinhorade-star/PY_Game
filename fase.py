"""Cenário das fases: plataformas, comprimento do mapa e fim da fase."""
import pygame

COR_CEU = (110, 170, 220)
COR_TERRA = (100, 70, 45)

# Cada fase é um dicionário. As plataformas são (x, y, largura, altura),
# em coordenadas do MUNDO (o mapa inteiro), não da tela.
FASES = [
    {
        "comprimento": 3000,
        "plataformas": [
            (0, 550, 3000, 50),     # chão
            (400, 450, 150, 20),
            (650, 400, 150, 20),
            (1100, 450, 200, 20),
            (1500, 420, 120, 20),
            (1700, 360, 160, 20),
            (2200, 450, 200, 20),
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
    """Monta o cenário de uma fase a partir da lista FASES."""

    def __init__(self, numero):
        """Cria a fase de índice numero (0 = primeira fase)."""
        dados = FASES[numero]
        self.numero = numero
        self.comprimento = dados["comprimento"]
        self.plataformas = pygame.sprite.Group()
        for x, y, largura, altura in dados["plataformas"]:
            self.plataformas.add(Plataforma(x, y, largura, altura))

    def atualizar(self):
        """Atualiza o que se mexe na fase (inimigos entram no próximo passo)."""
        pass

    def desenhar(self, tela, camera):
        """Desenha o céu e as plataformas, deslocados pela câmera."""
        tela.fill(COR_CEU)
        camera.desenhar_grupo(tela, self.plataformas)

    def terminou(self, jogador):
        """Retorna True quando o jogador chega ao fim do mapa."""
        return jogador.rect.right >= self.comprimento
