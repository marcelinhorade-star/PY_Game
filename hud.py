"""HUD: informações desenhadas por cima do jogo (vida, pontos e fase)."""
import pygame

import config


class HUD:
    """Desenha corações de vida no canto esquerdo, a fase no meio e os pontos na direita."""

    def __init__(self, vida_max):
        """vida_max é quantos corações desenhar (a vida com que o jogador começa)."""
        self.vida_max = vida_max
        self.fonte = pygame.font.Font(None, 36)

    def _coracao(self, tela, x, y, cheio):
        """Coração feito com 2 círculos e 1 triângulo: vermelho (vida) ou cinza escuro (perdida)."""
        cor = config.VERMELHO if cheio else (60, 60, 60)
        pygame.draw.circle(tela, cor, (x + 7, y + 7), 7)
        pygame.draw.circle(tela, cor, (x + 19, y + 7), 7)
        pygame.draw.polygon(tela, cor, [(x, y + 9), (x + 26, y + 9), (x + 13, y + 24)])

    def _texto(self, tela, texto, cor, **posicao):
        """Texto com sombra; posicao é, por exemplo, topright=(x, y)."""
        sombra = self.fonte.render(texto, True, config.PRETO)
        imagem = self.fonte.render(texto, True, cor)
        destino = imagem.get_rect(**posicao)
        tela.blit(sombra, destino.move(2, 2))
        tela.blit(imagem, destino)

    def desenhar(self, tela, vida, pontos, numero_fase):
        """Desenha o HUD. numero_fase começa em 0, mas mostramos 'FASE 1'."""
        for i in range(self.vida_max):
            self._coracao(tela, 16 + i * 34, 16, cheio=i < vida)
        self._texto(tela, f"FASE {numero_fase + 1}", config.BRANCO, midtop=(config.LARGURA // 2, 16))
        self._texto(tela, f"PONTOS {pontos:05d}", config.AMARELO, topright=(config.LARGURA - 16, 16))
