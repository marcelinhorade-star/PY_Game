"""Música de fundo e efeitos sonoros.

Sons de Juhani Junkala (SubspaceAudio), licença CC0, baixados do OpenGameArt.
Os créditos completos estão no README.
"""
import os

import pygame

import config

# nome usado no código -> arquivo dentro da pasta sons/
EFEITOS = {
    "tiro": "tiro.wav",
    "dano": "dano.wav",
    "inimigo_morre": "inimigo_morre.wav",
    "game_over": "game_over.wav",
    "vitoria": "vitoria.wav",
}
MUSICAS = {
    "menu": "musica_menu.wav",
    "fase": "musica_fase.wav",
}


class Som:
    """Carrega os sons uma vez e toca quando o jogo pede.

    Se o computador não tiver saída de áudio, o jogo continua sem som
    (self.ativo fica False e os métodos simplesmente não fazem nada).
    """

    def __init__(self):
        """Liga o mixer e carrega todos os efeitos na memória."""
        self.efeitos = {}
        self.musica_atual = None
        try:
            pygame.mixer.init()
        except pygame.error:
            self.ativo = False
            return
        self.ativo = True
        for nome, arquivo in EFEITOS.items():
            self.efeitos[nome] = pygame.mixer.Sound(os.path.join(config.PASTA_SONS, arquivo))
        self.efeitos["tiro"].set_volume(0.4)   # o tiro toca muito: mais baixo para não cansar

    def tocar(self, nome):
        """Toca um efeito uma vez (vários podem tocar ao mesmo tempo)."""
        if self.ativo:
            self.efeitos[nome].play()

    def tocar_musica(self, nome):
        """Troca a música de fundo e repete para sempre. Se já está tocando, não reinicia."""
        if not self.ativo or nome == self.musica_atual:
            return
        pygame.mixer.music.load(os.path.join(config.PASTA_SONS, MUSICAS[nome]))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)   # -1 = repetir sem parar
        self.musica_atual = nome

    def parar_musica(self):
        """Para a música de fundo."""
        if self.ativo:
            pygame.mixer.music.stop()
            self.musica_atual = None
