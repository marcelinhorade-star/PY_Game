"""Fases do jogo: cenário, plataformas, inimigos, comprimento do mapa e fim da fase."""
import pygame
import config
from inimigo import Inimigo, Atirador, Bazuca, carregar_assets_inimigos
from chefe import Chefe
from cenario import Camada, Tileset
from colisoes import tiros_inimigos_x_plataformas

# O jogador não pode passar mais que isso (em pixels) à frente do inimigo vivo
# mais atrasado. Assim ele não consegue correr direto para o fim do mapa: é
# preciso matar todos para avançar, inclusive os que estão em cima das
# plataformas. Para trás ele pode voltar à vontade (a câmera segue).
DISTANCIA_MAX_INIMIGO = 300

# Qual classe cria cada tipo de inimigo escrito na lista da fase.
TIPOS_INIMIGOS = {"soldado": Inimigo, "atirador": Atirador, "bazuca": Bazuca, "chefe": Chefe}

# Depois que o chefe morre, espera este tempo (ms) para as explosões tocarem
# antes de mostrar a tela de vitória.
ESPERA_DEPOIS_DO_CHEFE = 2000

# Cada fase é um dicionário. Tudo em coordenadas do MUNDO (o mapa inteiro):
# plataformas são (x, y, largura, altura) e inimigos são (tipo, x, y dos pés).
# "camadas" são as imagens de fundo e o quanto cada uma anda com a câmera.
# "tom" (opcional) é uma cor que multiplica as camadas: (255, 255, 255) não muda nada,
# cores mais escuras escurecem o fundo (a fase 3 usa isso para virar noite).
FASES = [
    {
        "comprimento": 3000,
        "cor_fundo": (20, 22, 18),
        "camadas": [("subway_BG.png", 0.3)],
        "tileset": "Subway_tiles.png",
        "plataformas": [
            # chão, com 3 buracos (cair num buraco tira 1 vida)
            (0, 550, 560, 50),
            (760, 550, 550, 50),    # buraco de 560 a 760: passe pelas plataformas
            (1450, 550, 970, 50),   # buraco de 1310 a 1450
            (2560, 550, 440, 50),   # buraco de 2420 a 2560
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
            # chão, com 3 buracos
            (0, 550, 960, 50),
            (1240, 550, 630, 50),   # buraco de 960 a 1240: passe pelas plataformas
            (1990, 550, 690, 50),   # buraco de 1870 a 1990
            (2890, 550, 710, 50),   # buraco de 2680 a 2890: desça da plataforma alta
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
    {
        # fase 3: de noite, com o chefe no fim (arena de 2340 a 3400, sem buracos)
        "comprimento": 3400,
        "inicio_arena": 2340,   # depois de entrar aqui, não dá para voltar até o chefe morrer
        "cor_fundo": (18, 16, 40),
        "camadas": [("nuvens_3.png", 0.05), ("nuvens_2.png", 0.15), ("nuvens_1.png", 0.3)],
        "tom": (70, 80, 255),
        "tileset": "Subway_tiles.png",
        "plataformas": [
            # chão, com 3 buracos
            (0, 550, 700, 50),
            (840, 550, 610, 50),    # buraco de 700 a 840: dá para pular
            (1700, 550, 500, 50),   # buraco de 1450 a 1700: use a plataforma do meio
            (2340, 550, 1060, 50),  # buraco de 2200 a 2340: dá para pular; depois é a arena
            (350, 440, 160, 32),
            (950, 440, 200, 32),
            (1510, 450, 130, 32),   # plataforma no meio do buraco largo
            (1800, 420, 160, 32),
            (2550, 420, 160, 32),   # na arena: proteção contra a chuva de foguetes
            (2950, 420, 160, 32),
        ],
        "inimigos": [
            ("soldado", 550, 550),
            ("atirador", 430, 440),
            ("soldado", 1050, 440),
            ("bazuca", 1300, 550),
            ("atirador", 1880, 420),
            ("soldado", 2000, 550),
            ("bazuca", 2150, 550),
            ("chefe", 3150, 550),
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
        if "tom" in dados:
            for camada in self.camadas:
                camada.imagem.fill(dados["tom"], special_flags=pygame.BLEND_RGB_MULT)

        tileset = Tileset(dados["tileset"])
        self.plataformas = pygame.sprite.Group()
        for x, y, largura, altura in dados["plataformas"]:
            self.plataformas.add(Plataforma(x, y, largura, altura, tileset))

        self.ponto_seguro = None    # último lugar com chão firme onde o jogador pisou
        self.inicio_arena = dados.get("inicio_arena")   # None nas fases sem chefe
        self.arena_fechada = False
        self.inimigos = pygame.sprite.Group()
        self.tiros_inimigos = pygame.sprite.Group()
        self.efeitos = pygame.sprite.Group()
        grupos = {"tiros_inimigos": self.tiros_inimigos, "efeitos": self.efeitos}
        assets = carregar_assets_inimigos()   # imagens carregadas uma vez só
        self.chefe = None           # só a última fase tem chefe
        for tipo, x, y in dados["inimigos"]:
            classe = TIPOS_INIMIGOS[tipo]
            inimigo = classe(x, y, assets, grupos)
            self.inimigos.add(inimigo)
            if tipo == "chefe":
                self.chefe = inimigo

    def atualizar(self, jogador):
        """Atualiza inimigos, tiros inimigos e efeitos (uma vez por quadro)."""
        # parede invisível: não deixa o jogador passar dos inimigos vivos
        if jogador.rect.right > self.limite_do_jogador():
            jogador.rect.right = self.limite_do_jogador()
        self.prender_na_arena(jogador)
        self.verificar_queda(jogador)
        self.inimigos.update(jogador, self.plataformas)
        self.tiros_inimigos.update()
        tiros_inimigos_x_plataformas(self.tiros_inimigos, self.plataformas)
        self.efeitos.update()

    def verificar_queda(self, jogador):
        """Buracos: se o jogador cair, perde 1 vida e volta para o último chão firme.

        Enquanto ele está em cima de uma plataforma (longe da beirada), guardamos
        a posição em ponto_seguro. Se ele passar da parte de baixo da tela, caiu.
        """
        if jogador.no_chao:
            x, y = jogador.rect.midbottom
            for plataforma in self.plataformas:
                longe_da_beirada = plataforma.rect.left + 40 < x < plataforma.rect.right - 40
                if plataforma.rect.top == y and longe_da_beirada:
                    self.ponto_seguro = (x, y)
        elif jogador.rect.top > config.ALTURA and jogador.esta_vivo():
            jogador.levar_dano()
            if jogador.esta_vivo():     # se morreu, deixa cair (main.py mostra o game over)
                jogador.rect.midbottom = self.ponto_seguro
                jogador.vel_y = 0

    def prender_na_arena(self, jogador):
        """Arena do chefe: quando o jogador entra nela, a arena fecha atrás dele.

        Só fecha se o chefe for o único inimigo vivo (senão o jogador ficaria
        preso longe de um inimigo esquecido). Abre de novo quando o chefe morre.
        """
        if self.inicio_arena is None or self.chefe is None:
            return
        if not self.chefe.alive():
            self.arena_fechada = False
            return
        if len(self.inimigos) == 1 and jogador.rect.left >= self.inicio_arena:
            self.arena_fechada = True
        if self.arena_fechada and jogador.rect.left < self.inicio_arena:
            jogador.rect.left = self.inicio_arena

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
        if self.chefe is not None and self.chefe.alive() and camera.esta_visivel(self.chefe.rect):
            self.chefe.desenhar_barra(tela)

    def terminou(self, jogador):
        """Retorna True quando a fase acabou.

        Fase com chefe: acaba um pouco depois de o chefe morrer.
        Fase sem chefe: acaba quando o jogador chega ao fim do mapa.
        """
        if self.chefe is not None:
            if self.chefe.morreu_em is None:
                return False
            return pygame.time.get_ticks() - self.chefe.morreu_em > ESPERA_DEPOIS_DO_CHEFE
        return jogador.rect.right >= self.comprimento


def existe_fase(numero):
    """Retorna True se existe uma fase com esse índice (para saber se o jogo acabou)."""
    return numero < len(FASES)
