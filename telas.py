"""Telas fora da partida: início, escolha de personagem, nome, game over e vitória.

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

# como a partida acabou -> (título, cor do título, cor do fundo)
FINAIS = {
    "game_over": ("GAME OVER", config.VERMELHO, (40, 10, 10)),
    "vitoria": ("VITÓRIA!", config.VERDE, (10, 40, 20)),
}


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

    def desenhar_inicio(self, tela, placar):
        """Título, recorde, 'aperte ENTER' piscando e a lista de controles.

        placar: lista de maiores pontuações (placar.py); o recorde é a primeira.
        """
        tela.fill((25, 28, 40))
        self._texto(tela, config.TITULO, self.fonte_titulo, config.AMARELO, 150)
        if placar:
            recorde = placar[0]
            self._texto(tela, f"Recorde: {recorde['nome']}  {recorde['pontos']} pontos",
                        self.fonte_pequena, config.BRANCO, 220)
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

    def desenhar_nome(self, tela, resultado, pontos, nome):
        """Fim da partida: mostra a pontuação e uma caixa com o nome sendo digitado.

        resultado: "game_over" ou "vitoria" (escolhe título e cores em FINAIS)
        nome: o que o jogador já digitou
        """
        titulo, cor, fundo = FINAIS[resultado]
        tela.fill(fundo)
        self._texto(tela, titulo, self.fonte_titulo, cor, 130)
        self._texto(tela, f"Pontos: {pontos}", self.fonte_media, config.BRANCO, 220)
        self._texto(tela, "Digite seu nome:", self.fonte_pequena, config.CINZA, 300)
        caixa = pygame.Rect(0, 0, 420, 60)
        caixa.center = (config.LARGURA // 2, 360)
        pygame.draw.rect(tela, (20, 20, 30), caixa)
        pygame.draw.rect(tela, config.AMARELO, caixa, 3)
        cursor = "_" if self._piscando() else " "   # tracinho piscando depois do nome
        self._texto(tela, nome + cursor, self.fonte_media, config.AMARELO, 360)
        self._texto(tela, "ENTER: salvar      BACKSPACE: apagar", self.fonte_pequena, config.CINZA, 450)

    def desenhar_placar(self, tela, resultado, pontos, placar, posicao):
        """Tela final: título, pontuação da partida e a tabela das maiores pontuações.

        placar: lista de dicionários com nome, pontos e personagem (placar.py)
        posicao: índice da pontuação desta partida no placar (fica amarela), ou None
        """
        titulo, cor, fundo = FINAIS[resultado]
        tela.fill(fundo)
        self._texto(tela, titulo, self.fonte_titulo, cor, 60)
        self._texto(tela, f"Pontos: {pontos}", self.fonte_media, config.BRANCO, 125)
        if posicao is None:
            self._texto(tela, "Não entrou no placar desta vez", self.fonte_pequena, config.CINZA, 160)
        self._texto(tela, "MELHORES PONTUAÇÕES", self.fonte_pequena, config.AMARELO, 195)
        # a fonte não é monoespaçada, então cada coluna é escrita numa posição x fixa
        for i, linha in enumerate(placar):
            y = 230 + i * 28
            cor_linha = config.AMARELO if i == posicao else config.BRANCO
            colunas = [
                (f"{i + 1}.", "topright", 300),
                (linha["nome"], "topleft", 320),
                (linha.get("personagem", ""), "topleft", 540),
                (str(linha["pontos"]), "topright", 680),
            ]
            for texto, ancora, x in colunas:
                imagem = self.fonte_pequena.render(texto, True, cor_linha)
                tela.blit(imagem, imagem.get_rect(**{ancora: (x, y)}))
        self._texto(tela, "ENTER para jogar de novo", self.fonte_pequena, config.CINZA, 560)
