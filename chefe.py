"""Chefe da última fase: um soldado gigante com barra de vida e 2 ataques.

O Chefe herda do Inimigo (inimigo.py), então anda, cai com a gravidade,
anima e morre do mesmo jeito. O que muda:
    - é maior (as imagens do soldado aumentadas 2 vezes) e tem muito mais vida;
    - alterna entre 2 ataques: RAJADA (3 tiros retos, baixos ou altos)
      e CHUVA (foguetes que caem do céu perto do jogador);
    - com metade da vida fica FURIOSO: fica vermelho e ataca mais rápido;
    - desenha uma barra de vida no topo da tela.

Sprites do pacote "Generic RUN n' GUN" (Vaca Roxa, licença CC0).
"""
import random
import pygame

import config
from inimigo import Inimigo
from efeitos import TiroInimigo, Foguete, Efeito

AUMENTO = 2   # o chefe é o soldado comum desenhado 2 vezes maior


def aumentar_animacoes(animacoes):
    """Devolve uma cópia do dicionário de animações com todas as imagens AUMENTO vezes maiores."""
    maiores = {}
    for nome, imagens in animacoes.items():
        if nome == "bala":   # "bala" é uma imagem só, as outras são listas de quadros
            maiores[nome] = pygame.transform.scale_by(imagens, AUMENTO)
        else:
            maiores[nome] = [pygame.transform.scale_by(quadro, AUMENTO) for quadro in imagens]
    return maiores


class FogueteCaindo(Foguete):
    """Foguete que cai reto do céu (ataque CHUVA). Explode no chão ou no jogador."""

    VELOCIDADE_QUEDA = 5

    def __init__(self, imagem, x, frames_explosao, grupo_efeitos):
        """Cria o foguete acima da tela, na coordenada x do mundo, apontando para baixo."""
        # rotate(-90) gira no sentido horário: o foguete, que aponta para a direita, passa a apontar para baixo
        apontando_para_baixo = pygame.transform.rotate(imagem, -90)
        super().__init__(apontando_para_baixo, x, -30, 0, frames_explosao, grupo_efeitos)
        self.vel_y = self.VELOCIDADE_QUEDA


class Chefe(Inimigo):
    """Soldado gigante do fim da fase 3. Só dá para vencer o jogo depois de matá-lo."""

    NOME = "soldado"             # usa as imagens do soldado comum (aumentadas)
    VIDA = 70
    VELOCIDADE = 1
    PONTOS = 2000
    DISTANCIA_VISAO = 700        # começa a lutar quando o jogador chega perto
    DISTANCIA_MINIMA = 320       # não chega mais perto que isso
    RAIO_PATRULHA = 60

    INTERVALO_ATAQUE = 1800      # ms entre o começo de um ataque e o próximo
    INTERVALO_RAJADA = 110       # ms entre os tiros de uma rajada (juntos: um pulo passa todos)
    VELOCIDADE_TIRO = 7
    ALTURA_TIRO_BAIXO = 14       # tiro baixo (acima dos pés): pule por cima
    ALTURA_TIRO_ALTO = 60        # tiro alto: agache para passar por baixo

    def __init__(self, x, y, assets, grupos):
        """Cria o chefe com os pés em (x, y). Os parâmetros são os mesmos do Inimigo."""
        super().__init__(x, y, assets, grupos)
        self.animacoes = aumentar_animacoes(assets[self.NOME])
        self.image = self.animacoes["parado"][0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vida_max = self.VIDA
        self.proximo_ataque = "rajada"
        self.rajada_alta = False      # alterna: uma rajada baixa, depois uma alta...
        self.tiros_restantes = 0      # tiros que ainda faltam na rajada atual
        self.ultimo_ataque = pygame.time.get_ticks()
        self.ultimo_dano = -10000     # para piscar branco quando leva tiro
        self.morreu_em = None         # momento (ms) da morte; a fase usa para terminar
        self.fonte = pygame.font.Font(None, 28)

    def esta_furioso(self):
        """True quando o chefe já perdeu metade da vida."""
        return self.vida <= self.vida_max // 2

    def intervalo_ataque(self):
        """Tempo entre ataques: furioso ele ataca mais rápido."""
        if self.esta_furioso():
            return self.INTERVALO_ATAQUE * 2 // 3
        return self.INTERVALO_ATAQUE

    # ------------------------------------------------------------ ataques
    def criar_tiro(self):
        """Um tiro reto da rajada, na altura baixa ou alta."""
        altura = self.ALTURA_TIRO_ALTO if self.rajada_alta else self.ALTURA_TIRO_BAIXO
        x = self.rect.centerx + self.direcao * self.rect.width // 3
        y = self.rect.bottom - altura
        return TiroInimigo(self.animacoes["bala"], x, y, self.VELOCIDADE_TIRO * self.direcao, 0)

    def comecar_rajada(self):
        """Ataque RAJADA: prepara 3 tiros (4 se furioso). Eles saem aos poucos no atirar()."""
        self.rajada_alta = not self.rajada_alta
        self.tiros_restantes = 4 if self.esta_furioso() else 3

    def chuva_de_foguetes(self, jogador):
        """Ataque CHUVA: foguetes caem do céu em volta do jogador (5 se furioso)."""
        if self.esta_furioso():
            distancias = [-240, -120, 0, 120, 240]
        else:
            distancias = [-150, 0, 150]
        desvio = random.randint(-30, 30)   # para não cair sempre no mesmo lugar
        for distancia in distancias:
            x = jogador.rect.centerx + distancia + desvio
            foguete = FogueteCaindo(self.assets["bazuca"]["bala"], x,
                                    self.assets["explosao"], self.grupos["efeitos"])
            self.grupos["tiros_inimigos"].add(foguete)

    def atirar(self, jogador):
        """Substitui o atirar do Inimigo: solta os tiros da rajada e escolhe o próximo ataque."""
        agora = pygame.time.get_ticks()
        # 1) se há uma rajada em andamento, solta o próximo tiro dela
        if self.tiros_restantes > 0 and agora - self.ultimo_tiro > self.INTERVALO_RAJADA:
            self.grupos["tiros_inimigos"].add(self.criar_tiro())
            self.tiros_restantes -= 1
            self.ultimo_tiro = agora
            self.atirando_ate = agora + len(self.animacoes["atirando"]) * self.frame_ticks
        # 2) de tempos em tempos começa um ataque novo, alternando entre os dois
        if self.distancia_ate(jogador) > self.DISTANCIA_VISAO:
            return
        if agora - self.ultimo_ataque > self.intervalo_ataque():
            if self.proximo_ataque == "rajada":
                self.comecar_rajada()
                self.proximo_ataque = "chuva"
            else:
                self.chuva_de_foguetes(jogador)
                self.proximo_ataque = "rajada"
            self.ultimo_ataque = agora

    # ------------------------------------------------------------ dano e desenho
    def levar_dano(self, quantidade=1):
        """Tira vida e pisca. Ao morrer, solta várias explosões e guarda a hora da morte."""
        self.ultimo_dano = pygame.time.get_ticks()
        morreu = super().levar_dano(quantidade)
        if morreu:
            self.morreu_em = pygame.time.get_ticks()
            for i in range(5):
                x = self.rect.left + random.randint(0, self.rect.width)
                y = self.rect.bottom - random.randint(0, self.rect.height // 2)
                self.grupos["efeitos"].add(Efeito(self.assets["explosao"], (x, y), frame_ticks=90 + 30 * i))
        return morreu

    def animar(self):
        """Anima como o Inimigo e depois pinta: vermelho se furioso, branco ao levar tiro."""
        super().animar()
        agora = pygame.time.get_ticks()
        if self.esta_furioso() or agora - self.ultimo_dano < 80:
            self.image = self.image.copy()   # copia para não estragar o quadro original
            if agora - self.ultimo_dano < 80:
                self.image.fill((120, 120, 120), special_flags=pygame.BLEND_RGB_ADD)
            else:
                self.image.fill((255, 120, 120), special_flags=pygame.BLEND_RGB_MULT)

    def desenhar_barra(self, tela):
        """Barra de vida no topo da tela, embaixo do texto da fase."""
        largura, altura = 400, 18
        x = (config.LARGURA - largura) // 2
        y = 72
        cheia = largura * self.vida // self.vida_max
        pygame.draw.rect(tela, (60, 60, 60), (x, y, largura, altura))
        pygame.draw.rect(tela, config.VERMELHO, (x, y, cheia, altura))
        pygame.draw.rect(tela, config.BRANCO, (x, y, largura, altura), 2)   # 2 = só a borda
        nome = self.fonte.render("COMANDANTE", True, config.BRANCO)
        tela.blit(nome, nome.get_rect(midbottom=(config.LARGURA // 2, y - 2)))
