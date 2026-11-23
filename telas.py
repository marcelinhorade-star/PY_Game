"""Telas fora da partida: início, escolha de personagem, game over e vitória.

Aqui só se DESENHA. Quem decide qual tela mostrar e o que cada tecla faz é
a máquina de estados do main.py.
"""
import pygame

import config
from tiro import ARMAS

CONTROLES = [
    "Setas: andar",
    "Seta para cima: mirar para cima      Seta para baixo: agachar",
    "Espaço: pular      Z: atirar",
]


class Telas:
    """Guarda as fontes (carregar fonte é lento, então fazemos uma vez só) e desenha cada tela."""

    def __init__(self):
        """Cria as fontes nos três tamanhos usados."""
        self.fonte_titulo = pygame.font.Font(None, 96)
        self.fonte_media = pygame.font.Font(None, 48)
        self.fonte_pequena = pygame.font.Font(None, 30)

    def _texto(self, tela, texto, fonte, cor, centro_y):
        """Escreve um texto centralizado na horizontal, com uma sombra preta atrás."""
        x = config.LARGURA // 2
        sombra = fonte.render(texto, True, config.PRETO)
        tela.blit(sombra, sombra.get_rect(center=(x + 3, centro_y + 3)))
        imagem = fonte.render(texto, True, cor)
        tela.blit(imagem, imagem.get_rect(center=(x, centro_y)))

    def _piscando(self):
        """True em metade do tempo: troca a cada 500 ms (para o 'aperte ENTER')."""
        return (pygame.time.get_ticks() // 500) % 2 == 0

    def desenhar_inicio(self, tela):
        """Título, 'aperte ENTER' piscando e a lista de controles."""
        tela.fill((25, 28, 40))
        self._texto(tela, config.TITULO, self.fonte_titulo, config.AMARELO, 150)
        if self._piscando():
            self._texto(tela, "Aperte ENTER para jogar", self.fonte_media, config.BRANCO, 290)
        for i, linha in enumerate(CONTROLES):
            self._texto(tela, linha, self.fonte_pequena, config.CINZA, 400 + i * 36)

    def desenhar_escolha(self, tela, personagens, retratos, escolhido):
        """Mostra os personagens lado a lado; o escolhido fica com moldura amarela.

        personagens: lista PERSONAGENS (personagens.py)
        retratos: uma imagem de cada personagem, na mesma ordem
        escolhido: índice do personagem marcado agora
        """
        tela.fill((25, 28, 40))
        self._texto(tela, "Escolha o personagem", self.fonte_media, config.AMARELO, 60)
        largura_caixa = 260
        espaco = (config.LARGURA - largura_caixa * len(personagens)) // (len(personagens) + 1)
        for i, personagem in enumerate(personagens):
            x = espaco + i * (largura_caixa + espaco)
            caixa = pygame.Rect(x, 110, largura_caixa, 330)
            cor = config.AMARELO if i == escolhido else config.CINZA
            pygame.draw.rect(tela, (40, 44, 60), caixa)
            pygame.draw.rect(tela, cor, caixa, 4 if i == escolhido else 2)
            # retrato aumentado mais 2 vezes, com os pés perto do meio da caixa
            retrato = pygame.transform.scale_by(retratos[i], 2)
            tela.blit(retrato, retrato.get_rect(midbottom=(caixa.centerx, caixa.top + 170)))
            linhas = [
                (personagem["nome"], self.fonte_media, cor),
                (f"Vida: {personagem['vida']}", self.fonte_pequena, config.BRANCO),
                (f"Arma: {ARMAS[personagem['arma']]['nome']}", self.fonte_pequena, config.BRANCO),
                (f"Velocidade: {personagem['velocidade']}", self.fonte_pequena, config.BRANCO),
            ]
            y = caixa.top + 200
            for texto, fonte, cor_texto in linhas:
                imagem = fonte.render(texto, True, cor_texto)
                tela.blit(imagem, imagem.get_rect(center=(caixa.centerx, y)))
                y += 34
        self._texto(tela, personagens[escolhido]["descricao"], self.fonte_pequena, config.BRANCO, 480)
        self._texto(tela, "Setas: trocar      ENTER: jogar", self.fonte_pequena, config.CINZA, 540)

    def desenhar_game_over(self, tela, pontos):
        """Tela de derrota com a pontuação."""
        tela.fill((40, 10, 10))
        self._texto(tela, "GAME OVER", self.fonte_titulo, config.VERMELHO, 200)
        self._texto(tela, f"Pontos: {pontos}", self.fonte_media, config.BRANCO, 300)
        self._texto(tela, "ENTER para jogar de novo", self.fonte_pequena, config.CINZA, 400)

    def desenhar_vitoria(self, tela, pontos):
        """Tela de vitória com a pontuação."""
        tela.fill((10, 40, 20))
        self._texto(tela, "VITÓRIA!", self.fonte_titulo, config.VERDE, 200)
        self._texto(tela, f"Pontos: {pontos}", self.fonte_media, config.BRANCO, 300)
        self._texto(tela, "ENTER para jogar de novo", self.fonte_pequena, config.CINZA, 400)
