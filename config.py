"""Constantes compartilhadas por todo o grupo: tela, tempo, cores e pastas.

Qualquer arquivo pode usar assim:

    import config
    tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
"""
import os

# ---------------------------------------------------------------- Janela
TITULO = "PY Game"
LARGURA = 960      # largura da janela em pixels
ALTURA = 600       # altura da janela (o chão das fases fica em y = 550 e tem 50 px)
FPS = 60           # quadros por segundo (usado no clock.tick)

# ---------------------------------------------------------------- Cores (R, G, B)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (120, 120, 120)
VERMELHO = (210, 50, 50)
VERDE = (60, 190, 80)
AMARELO = (245, 200, 60)

# ---------------------------------------------------------------- Pastas
# os.path.dirname(__file__) é a pasta onde este arquivo está. Assim os caminhos
# funcionam mesmo que o jogo seja rodado a partir de outra pasta.
PASTA_JOGO = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA_JOGO, "imagens")
PASTA_SONS = os.path.join(PASTA_JOGO, "sons")
