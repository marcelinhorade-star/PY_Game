"""Câmera que acompanha o jogador no eixo x."""


class Camera:
    """Guarda quanto o mundo está deslocado em x e desenha tudo com esse desvio.

    Como no Metal Slug, a câmera só anda para a frente: o jogador nunca volta
    para trás da borda esquerda da tela.
    """

    def __init__(self, largura_tela, comprimento_fase):
        """Cria a câmera no começo do mapa."""
        self.x = 0
        self.largura_tela = largura_tela
        self.comprimento_fase = comprimento_fase

    def atualizar(self, jogador):
        """Avança a câmera quando o jogador passa de 1/3 da tela e o prende nas bordas."""
        alvo = jogador.rect.centerx - self.largura_tela // 3
        maximo = self.comprimento_fase - self.largura_tela
        if alvo > self.x:
            self.x = min(alvo, maximo)
        if jogador.rect.left < self.x:
            jogador.rect.left = self.x
        if jogador.rect.right > self.comprimento_fase:
            jogador.rect.right = self.comprimento_fase

    def aplicar(self, rect):
        """Converte um rect do mundo para a posição dele na tela."""
        return rect.move(-self.x, 0)

    def esta_visivel(self, rect):
        """Retorna True se o rect aparece (mesmo que em parte) na tela."""
        return rect.right > self.x and rect.left < self.x + self.largura_tela

    def desenhar_grupo(self, tela, grupo):
        """Desenha cada sprite do grupo na posição deslocada pela câmera."""
        for sprite in grupo:
            tela.blit(sprite.image, self.aplicar(sprite.rect))
