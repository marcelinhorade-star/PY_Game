"""Câmera que acompanha o jogador no eixo x."""


class Camera:
    """Guarda quanto o mundo está deslocado em x e desenha tudo com esse desvio.

    A câmera segue o jogador para os dois lados (ele pode voltar no mapa),
    mas nunca mostra nada antes do começo nem depois do fim da fase.
    """

    def __init__(self, largura_tela, comprimento_fase):
        """Cria a câmera no começo do mapa."""
        self.x = 0
        self.largura_tela = largura_tela
        self.comprimento_fase = comprimento_fase

    def atualizar(self, jogador):
        """Deixa o jogador a 1/3 da tela (sobra mais espaço para ver à frente).

        A câmera vai para a frente e para trás junto com o jogador, mas fica
        presa entre 0 e o fim do mapa. O jogador também não sai do mapa.
        """
        if jogador.rect.left < 0:
            jogador.rect.left = 0
        if jogador.rect.right > self.comprimento_fase:
            jogador.rect.right = self.comprimento_fase
        alvo = jogador.rect.centerx - self.largura_tela // 3
        maximo = self.comprimento_fase - self.largura_tela
        self.x = max(0, min(alvo, maximo))   # prende o alvo entre 0 e maximo

    def aplicar(self, rect):
        """Converte um rect do mundo para a posição dele na tela."""
        return rect.move(-self.x, 0)

    def esta_visivel(self, rect):
        """Retorna True se o rect aparece (mesmo que em parte) na tela."""
        return rect.right > self.x and rect.left < self.x + self.largura_tela

    def remover_fora_da_tela(self, grupo):
        """Apaga os sprites do grupo que saíram da área visível (ex.: tiros perdidos)."""
        for sprite in grupo:
            if not self.esta_visivel(sprite.rect):
                sprite.kill()

    def desenhar_grupo(self, tela, grupo):
        """Desenha cada sprite do grupo na posição deslocada pela câmera."""
        for sprite in grupo:
            tela.blit(sprite.image, self.aplicar(sprite.rect))
