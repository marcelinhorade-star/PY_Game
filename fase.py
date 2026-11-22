"""Fases do jogo: cenário, plataformas, inimigos, comprimento do mapa e fim da fase."""
import pygame
from inimigo import Inimigo, Atirador, Bazuca, carregar_assets_inimigos
from cenario import Camada, Tileset
from colisoes import tiros_inimigos_x_plataformas

# O jogador não pode passar mais que isso (em pixels) à frente do inimigo vivo
# mais atrasado. Como a câmera só anda para a frente, isso garante que nenhum
# inimigo fica para trás fora da tela: é preciso matar todos para avançar,
# inclusive os que estão em cima das plataformas.
DISTANCIA_MAX_INIMIGO = 300

# Qual classe cria cada tipo de inimigo escrito na lista da fase.
TIPOS_INIMIGOS = {"soldado": Inimigo, "atirador": Atirador, "bazuca": Bazuca}

# Cada fase é um dicionário. Tudo em coordenadas do MUNDO (o mapa inteiro):
# plataformas são (x, y, largura, altura) e inimigos são (tipo, x, y dos pés).
# "camadas" são as imagens de fundo e o quanto cada uma anda com a câmera.
FASES = [
    {
        "comprimento": 3000,
        "cor_fundo": (20, 22, 18),
        "camadas": [("subway_BG.png", 0.3)],
        "tileset": "Subway_tiles.png",
        "plataformas": [
            (0, 550, 3000, 50),     # chão
            (400, 450, 150, 32),
            (650, 400, 150, 32),
            (1100, 450, 200, 32),
            (1500, 420, 128, 32),
            (1700, 360, 160, 32),
            (2200, 450, 200, 32),
        ],
        "inimigos": [
            ("soldado", 900, 550),
            ("soldado", 725, 400),
            ("bazuca", 1200, 450),
            ("atirador", 1780, 360),
            ("soldado", 2000, 550),
            ("bazuca", 2300, 450),
            ("soldado", 2700, 550),
        ],
    },
    {
        "comprimento": 3600,
        "cor_fundo": (250, 175, 130),
        "camadas": [("nuvens_3.png", 0.05), ("nuvens_2.png", 0.15), ("nuvens_1.png", 0.3)],
        "tileset": "tiles_out.png",
        "plataformas": [
            (0, 550, 3600, 50),     # chão
            (300, 460, 128, 32),
            (500, 390, 128, 32),
            (750, 450, 200, 32),
            (1050, 400, 160, 32),
            (1300, 340, 160, 32),
            (1600, 450, 256, 32),
            (2000, 420, 160, 32),
            (2250, 360, 160, 32),
            (2500, 300, 160, 32),
            (2900, 450, 320, 32),
        ],
        "inimigos": [
            ("soldado", 600, 550),
            ("soldado", 850, 450),
            ("bazuca", 1130, 400),
            ("atirador", 1380, 340),
            ("soldado", 1725, 450),
            ("soldado", 2400, 550),
            ("atirador", 2080, 420),
            ("bazuca", 2580, 300),
            ("atirador", 3050, 450),
            ("soldado", 3300, 550),
            ("bazuca", 3450, 550),
        ],
    },
]


class Plataforma(pygame.sprite.Sprite):
    """Bloco sólido onde o jogador e os inimigos podem ficar em cima."""

    def __init__(self, x, y, largura, altura, tileset):
        """Cria a plataforma com o canto superior esquerdo em (x, y), desenhada com o tileset."""
        super().__init__()
        self.image = tileset.montar(largura, altura)
        self.rect = self.image.get_rect(topleft=(x, y))


class Fase:
    """Monta o cenário de uma fase a partir da lista FASES e cuida dos inimigos."""

    def __init__(self, numero):
        """Cria a fase de índice numero (0 = primeira fase)."""
        dados = FASES[numero]
        self.numero = numero
        self.comprimento = dados["comprimento"]
        self.cor_fundo = dados["cor_fundo"]
        self.camadas = [Camada(arquivo, fator) for arquivo, fator in dados["camadas"]]

        tileset = Tileset(dados["tileset"])
        self.plataformas = pygame.sprite.Group()
        for x, y, largura, altura in dados["plataformas"]:
            self.plataformas.add(Plataforma(x, y, largura, altura, tileset))

        self.inimigos = pygame.sprite.Group()
        self.tiros_inimigos = pygame.sprite.Group()
        self.efeitos = pygame.sprite.Group()
        grupos = {"tiros_inimigos": self.tiros_inimigos, "efeitos": self.efeitos}
        assets = carregar_assets_inimigos()   # imagens carregadas uma vez só
        for tipo, x, y in dados["inimigos"]:
            classe = TIPOS_INIMIGOS[tipo]
            self.inimigos.add(classe(x, y, assets, grupos))

    def atualizar(self, jogador):
        """Atualiza inimigos, tiros inimigos e efeitos (uma vez por quadro)."""
        # parede invisível: não deixa o jogador passar dos inimigos vivos
        if jogador.rect.right > self.limite_do_jogador():
            jogador.rect.right = self.limite_do_jogador()
        self.inimigos.update(jogador, self.plataformas)
        self.tiros_inimigos.update()
        tiros_inimigos_x_plataformas(self.tiros_inimigos, self.plataformas)
        self.efeitos.update()

    def limite_do_jogador(self):
        """Até onde (x) o jogador pode andar para a direita agora.

        Enquanto houver inimigo vivo, o limite é o inimigo mais à esquerda mais
        DISTANCIA_MAX_INIMIGO. Sem inimigos, é o fim do mapa.
        """
        if len(self.inimigos) == 0:
            return self.comprimento
        mais_atrasado = min(inimigo.rect.centerx for inimigo in self.inimigos)
        return mais_atrasado + DISTANCIA_MAX_INIMIGO

    def desenhar(self, tela, camera):
        """Desenha o fundo (com parallax) e tudo da fase, deslocado pela câmera."""
        tela.fill(self.cor_fundo)
        for camada in self.camadas:
            camada.desenhar(tela, camera)
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
