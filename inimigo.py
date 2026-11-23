"""Inimigos do jogo: o soldado (classe base Inimigo), o Atirador e o Bazuca.

Sprites do pacote "Generic RUN n' GUN" (Vaca Roxa, licença CC0).
"""
import os
import pygame
from colisoes import altura_do_chao
from efeitos import TiroInimigo, Foguete, Efeito

PASTA_INIMIGOS = os.path.join(os.path.dirname(__file__), "imagens", "inimigos")
ESCALA = 2

# Cada folha de sprites é uma tira de quadros do mesmo tamanho, lado a lado.
# Para cada inimigo: o arquivo, a largura de um quadro e quais quadros formam
# cada animação (contando da esquerda, começando em 0). "bala" é o quadro
# que tem só o desenho do tiro.
FOLHAS = {
    "soldado": {
        "arquivo": "ARMob.png", "largura": 32,
        "parado": [0, 1, 2], "andando": [11, 12, 13, 14, 15, 16, 17, 18],
        "atirando": [3, 4], "morrendo": [19, 20, 21, 22], "bala": 23,
    },
    "atirador": {
        "arquivo": "SniperMob.png", "largura": 44,
        "parado": [0], "andando": [0],
        "atirando": [1, 2, 3, 4, 5, 6, 7, 8], "morrendo": [9, 10, 11, 12], "bala": 13,
    },
    "bazuca": {
        "arquivo": "RPGmob.png", "largura": 44,
        "parado": [0], "andando": [0],
        "atirando": [1, 2, 3, 4], "morrendo": [5, 6, 7, 8], "bala": 9,
    },
}
ANIMACOES = ["parado", "andando", "atirando", "morrendo"]


def carregar_quadros(arquivo, largura):
    """Corta uma folha de sprites em quadros de mesma largura e aumenta cada um."""
    folha = pygame.image.load(os.path.join(PASTA_INIMIGOS, arquivo)).convert_alpha()
    quadros = []
    for x in range(0, folha.get_width(), largura):
        quadro = folha.subsurface((x, 0, largura, folha.get_height()))
        quadros.append(pygame.transform.scale_by(quadro, ESCALA))
    return quadros


def recortar(imagem):
    """Devolve só a parte desenhada da imagem (tira a borda transparente)."""
    return imagem.subsurface(imagem.get_bounding_rect()).copy()


def carregar_assets_inimigos():
    """Carrega UMA vez as animações de todos os inimigos e da explosão.

    Os inimigos recebem este dicionário pronto, em vez de cada um carregar as
    próprias imagens (mesma ideia do dicionário assets do handout).
    """
    assets = {}
    for nome, folha in FOLHAS.items():
        quadros = carregar_quadros(folha["arquivo"], folha["largura"])
        animacoes = {}
        for animacao in ANIMACOES:
            animacoes[animacao] = [quadros[i] for i in folha[animacao]]
        animacoes["bala"] = recortar(quadros[folha["bala"]])
        assets[nome] = animacoes
    # os 2 primeiros quadros da explosão são só um círculo; usamos o resto
    assets["explosao"] = carregar_quadros("Explosion_Particle.png", 32)[2:]
    return assets


class Inimigo(pygame.sprite.Sprite):
    """Soldado que patrulha, persegue o jogador quando ele chega perto e atira."""

    NOME = "soldado"            # chave das animações em assets
    VIDA = 4                    # era 3
    VELOCIDADE = 2              # era 1
    PONTOS = 100
    DISTANCIA_VISAO = 400       # a partir daqui ele vê o jogador (era 350)
    DISTANCIA_MINIMA = 180      # para de chegar perto e só atira
    RAIO_PATRULHA = 100
    INTERVALO_TIRO = 1100       # ms entre um tiro e outro (era 1500)
    VELOCIDADE_TIRO = 7         # era 6
    ALTURA_ARMA = 42            # altura do cano da arma, medida a partir dos pés

    def __init__(self, x, y, assets, grupos):
        """Cria o inimigo com os pés em (x, y).

        assets: dicionário de carregar_assets_inimigos().
        grupos: dicionário com os grupos "tiros_inimigos" e "efeitos".
        """
        super().__init__()
        self.assets = assets
        self.grupos = grupos
        self.animacoes = assets[self.NOME]
        self.estado = "parado"
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 120
        self.image = self.animacoes["parado"][0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.x_inicial = x
        self.vida = self.VIDA
        self.direcao = -1
        self.vel_y = 0
        self.andando = False
        self.ultimo_tiro = pygame.time.get_ticks()
        self.atirando_ate = 0       # até quando mostrar a animação de tiro

    def distancia_ate(self, jogador):
        """Distância horizontal (em pixels) até o jogador."""
        return abs(jogador.rect.centerx - self.rect.centerx)

    def tem_chao_a_frente(self, plataformas):
        """True se o próximo passo ainda tem chão (para não cair da plataforma)."""
        frente = self.rect.move(self.direcao * self.rect.width, 0)
        return altura_do_chao(frente, plataformas) == self.rect.bottom

    def mover(self, jogador, plataformas):
        """Persegue o jogador se ele estiver perto; senão, patrulha."""
        x_antes = self.rect.x
        if self.distancia_ate(jogador) < self.DISTANCIA_VISAO:
            self.direcao = 1 if jogador.rect.centerx > self.rect.centerx else -1
            longe = self.distancia_ate(jogador) > self.DISTANCIA_MINIMA
            if longe and self.tem_chao_a_frente(plataformas):
                self.rect.x += self.VELOCIDADE * 2 * self.direcao
        elif self.VELOCIDADE > 0:
            saiu_da_area = abs(self.rect.centerx - self.x_inicial) > self.RAIO_PATRULHA
            voltando = (self.x_inicial - self.rect.centerx) * self.direcao > 0
            if (saiu_da_area and not voltando) or not self.tem_chao_a_frente(plataformas):
                self.direcao *= -1
            self.rect.x += self.VELOCIDADE * self.direcao
        self.andando = self.rect.x != x_antes

    def aplicar_gravidade(self, plataformas):
        """Puxa o inimigo para baixo até a plataforma embaixo dele."""
        chao = altura_do_chao(self.rect, plataformas)
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= chao:
            self.rect.bottom = chao
            self.vel_y = 0

    def criar_tiro(self):
        """Cria o tiro do soldado: reto, saindo do cano da arma."""
        x = self.rect.centerx + self.direcao * self.rect.width // 2
        y = self.rect.bottom - self.ALTURA_ARMA
        return TiroInimigo(self.animacoes["bala"], x, y, self.VELOCIDADE_TIRO * self.direcao, 0)

    def atirar(self, jogador):
        """Atira de INTERVALO_TIRO em INTERVALO_TIRO ms enquanto vê o jogador."""
        agora = pygame.time.get_ticks()
        vendo = self.distancia_ate(jogador) < self.DISTANCIA_VISAO
        if vendo and agora - self.ultimo_tiro > self.INTERVALO_TIRO:
            self.grupos["tiros_inimigos"].add(self.criar_tiro())
            self.ultimo_tiro = agora
            self.atirando_ate = agora + len(self.animacoes["atirando"]) * self.frame_ticks

    def animar(self):
        """Escolhe a animação (parado, andando ou atirando) e troca de frame com o tempo."""
        agora = pygame.time.get_ticks()
        if agora < self.atirando_ate:
            novo = "atirando"
        elif self.andando:
            novo = "andando"
        else:
            novo = "parado"
        if novo != self.estado:
            self.estado = novo
            self.frame = 0
        frames = self.animacoes[self.estado]
        if agora - self.last_update > self.frame_ticks:
            self.last_update = agora
            self.frame = (self.frame + 1) % len(frames)
        imagem = frames[self.frame]
        if self.direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        self.image = imagem
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def levar_dano(self, quantidade=1):
        """Tira vida. Se zerar, toca a animação de morte, some e retorna True."""
        self.vida -= quantidade
        if self.vida <= 0:
            frames = self.animacoes["morrendo"]
            if self.direcao == -1:
                frames = [pygame.transform.flip(f, True, False) for f in frames]
            self.grupos["efeitos"].add(Efeito(frames, self.rect.midbottom, frame_ticks=120))
            self.kill()
            return True
        return False

    def update(self, jogador, plataformas):
        """Atualiza o inimigo uma vez por quadro."""
        self.mover(jogador, plataformas)
        self.aplicar_gravidade(plataformas)
        self.atirar(jogador)
        self.animar()


class Atirador(Inimigo):
    """Sniper: fica parado, enxerga de longe e dá tiros rápidos.

    Herda tudo do Inimigo; só muda os números da classe.
    """

    NOME = "atirador"
    VIDA = 3                    # era 2
    VELOCIDADE = 0
    PONTOS = 150
    DISTANCIA_VISAO = 600       # era 550
    INTERVALO_TIRO = 1700       # era 2200
    VELOCIDADE_TIRO = 12        # era 10
    ALTURA_ARMA = 36


class Bazuca(Inimigo):
    """Soldado com bazuca: parado, aguenta mais tiros e dispara foguetes que explodem.

    Herda do Inimigo e sobrescreve criar_tiro para atirar um Foguete.
    """

    NOME = "bazuca"
    VIDA = 6                    # era 4
    VELOCIDADE = 0
    PONTOS = 200
    DISTANCIA_VISAO = 500       # era 450
    INTERVALO_TIRO = 2000       # era 2600
    VELOCIDADE_TIRO = 5         # era 4
    ALTURA_ARMA = 48

    def criar_tiro(self):
        """Cria um foguete, que explode quando bate no jogador ou numa plataforma."""
        x = self.rect.centerx + self.direcao * self.rect.width // 2
        y = self.rect.bottom - self.ALTURA_ARMA
        return Foguete(self.animacoes["bala"], x, y, self.VELOCIDADE_TIRO * self.direcao,
                       self.assets["explosao"], self.grupos["efeitos"])
