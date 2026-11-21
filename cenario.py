"""Imagens do cenário: fundo com parallax e plataformas montadas com tiles.

As imagens são do pacote "Generic RUN n' GUN" (Vaca Roxa, licença CC0).
"""
import os
import pygame

PASTA_CENARIO = os.path.join(os.path.dirname(__file__), "imagens", "cenario")

# Os desenhos originais são pequenos (pixel art), então aumentamos 2 vezes,
# igual ao jogador.
ESCALA = 2
TAMANHO_TILE = 16 * ESCALA

# Os tilesets do pacote têm um bloco em forma de cruz no canto (5x5 tiles).
# Dele tiramos 9 pedaços: (coluna, linha) de cada um, em tiles de 16 px.
PEDACOS = {
    ("esquerda", "topo"): (0, 1), ("meio", "topo"): (2, 0), ("direita", "topo"): (4, 1),
    ("esquerda", "meio"): (0, 2), ("meio", "meio"): (2, 2), ("direita", "meio"): (4, 2),
    ("esquerda", "base"): (0, 3), ("meio", "base"): (2, 4), ("direita", "base"): (4, 3),
}


def carregar_imagem(nome):
    """Carrega uma imagem da pasta do cenário, já aumentada pela ESCALA."""
    imagem = pygame.image.load(os.path.join(PASTA_CENARIO, nome)).convert_alpha()
    return pygame.transform.scale_by(imagem, ESCALA)


class Camada:
    """Imagem de fundo que se repete na horizontal e anda mais devagar que a câmera.

    fator = 0 deixa a camada parada; fator = 1 faz ela andar junto com o chão.
    Valores no meio dão a sensação de profundidade (parallax).
    """

    def __init__(self, nome_arquivo, fator):
        """Carrega a imagem da camada e guarda o fator de velocidade."""
        self.imagem = carregar_imagem(nome_arquivo)
        self.fator = fator

    def desenhar(self, tela, camera):
        """Desenha a camada repetida, deslocada por camera.x vezes o fator."""
        largura = self.imagem.get_width()
        y = tela.get_height() - self.imagem.get_height()   # encostada embaixo
        x = -(int(camera.x * self.fator) % largura)
        while x < tela.get_width():
            tela.blit(self.imagem, (x, y))
            x += largura


class Tileset:
    """Recorta os 9 pedaços de um tileset e monta imagens de plataformas."""

    def __init__(self, nome_arquivo):
        """Carrega o tileset e separa os pedaços descritos em PEDACOS."""
        imagem = carregar_imagem(nome_arquivo)
        self.pedacos = {}
        for posicao, (coluna, linha) in PEDACOS.items():
            recorte = (coluna * TAMANHO_TILE, linha * TAMANHO_TILE, TAMANHO_TILE, TAMANHO_TILE)
            self.pedacos[posicao] = imagem.subsurface(recorte)

    def montar(self, largura, altura):
        """Cria a imagem de uma plataforma de largura x altura repetindo os tiles.

        As bordas usam os pedaços de quina e de lado; o resto usa o miolo.
        """
        imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
        colunas = max(1, -(-largura // TAMANHO_TILE))   # divisão arredondando para cima
        linhas = max(1, -(-altura // TAMANHO_TILE))
        for c in range(colunas):
            for l in range(linhas):
                horizontal = "esquerda" if c == 0 else "direita" if c == colunas - 1 else "meio"
                vertical = "topo" if l == 0 else "base" if l == linhas - 1 else "meio"
                # a última coluna/linha encosta na borda (pode sobrepor a anterior)
                x = max(0, min(c * TAMANHO_TILE, largura - TAMANHO_TILE))
                y = max(0, min(l * TAMANHO_TILE, altura - TAMANHO_TILE))
                imagem.blit(self.pedacos[(horizontal, vertical)], (x, y))
        return imagem
