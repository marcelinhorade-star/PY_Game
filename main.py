"""Ponto de entrada do jogo. Para jogar: python main.py

A classe Jogo guarda o estado atual do jogo e repete, 60 vezes por segundo:
    1. tratar_eventos()  -> lê teclado e janela
    2. atualizar()       -> move tudo e resolve colisões (só no estado "jogando")
    3. desenhar()        -> pinta a tela do estado atual

Estados:  "inicio" -> "jogando" -> "game_over" ou "vitoria" -> "inicio" ...
São 3 fases (lista FASES do fase.py); a vitória vem depois de matar o chefe da fase 3.
"""
import pygame

import config
from jogador import Jogador
from fase import Fase, existe_fase
from camera import Camera
from colisoes import altura_do_chao, tiros_do_jogador_x_inimigos, inimigos_x_jogador
from telas import Telas
from hud import HUD
from som import Som

POSICAO_INICIAL = (100, 550)   # pés do jogador no começo de cada fase (chão em y = 550)
ESPERA_GAME_OVER = 1500        # ms entre a morte e a tela de game over (animação de morte)
VIDAS_POR_FASE = 2             # vidas que o jogador recupera ao entrar numa fase nova


class Jogo:
    """Controla a janela, o loop principal e a troca entre as telas do jogo."""

    def __init__(self):
        """Abre a janela e começa na tela de início."""
        pygame.init()
        pygame.display.set_caption(config.TITULO)
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        self.clock = pygame.time.Clock()
        self.telas = Telas()
        self.som = Som()
        self.pontos = 0
        self.rodando = True
        self.mudar_estado("inicio")

    def mudar_estado(self, novo):
        """Troca de estado e cuida da música/efeito de cada tela."""
        self.estado = novo
        if novo == "inicio":
            self.som.tocar_musica("menu")
        elif novo == "jogando":
            self.som.tocar_musica("fase")
        elif novo in ("game_over", "vitoria"):
            self.som.parar_musica()
            self.som.tocar(novo)   # os efeitos se chamam "game_over" e "vitoria"

    # ------------------------------------------------------------ partida
    def nova_partida(self):
        """Zera pontos, cria o jogador e carrega a primeira fase."""
        self.pontos = 0
        self.jogador = Jogador(*POSICAO_INICIAL)
        self.hud = HUD(self.jogador.vida)   # tantos corações quanto a vida inicial
        self.tiros_jogador = pygame.sprite.Group()
        self.morreu_em = None        # momento (ms) em que a vida chegou a 0
        self.carregar_fase(0)
        self.mudar_estado("jogando")

    def carregar_fase(self, numero):
        """Cria a fase e a câmera, põe o jogador de volta no começo do mapa e devolve 2 vidas."""
        self.numero_fase = numero
        self.fase = Fase(numero)
        self.camera = Camera(config.LARGURA, self.fase.comprimento)
        self.jogador.rect.midbottom = POSICAO_INICIAL
        self.tiros_jogador.empty()
        # recupera um pouco de vida a cada fase (sem passar da vida máxima do HUD)
        self.jogador.vida = min(self.jogador.vida + VIDAS_POR_FASE, self.hud.vida_max)

    # ------------------------------------------------------------ loop
    def rodar(self):
        """Loop principal: roda até o jogador fechar a janela."""
        while self.rodando:
            self.tratar_eventos()
            if self.estado == "jogando":
                self.atualizar()
            self.desenhar()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        pygame.quit()

    def tratar_eventos(self):
        """Teclas que valem um toque só (ENTER, espaço). Andar e atirar são lidos no atualizar."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if self.estado == "inicio" and evento.key == pygame.K_RETURN:
                    self.nova_partida()
                elif self.estado == "jogando" and evento.key == pygame.K_SPACE:
                    self.jogador.pular()
                elif self.estado in ("game_over", "vitoria") and evento.key == pygame.K_RETURN:
                    self.mudar_estado("inicio")   # jogar de novo

    def atualizar(self):
        """Um quadro de jogo: move, testa colisões e decide se a fase/partida acabou."""
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_z]:
            antes = len(self.tiros_jogador)
            self.jogador.atirar(self.tiros_jogador)   # o intervalo de 250 ms fica no Jogador
            if len(self.tiros_jogador) > antes:       # atirar() não diz se atirou: contamos os tiros
                self.som.tocar("tiro")

        chao_y = altura_do_chao(self.jogador.rect, self.fase.plataformas)
        self.jogador.update(teclas, chao_y)
        self.tiros_jogador.update()
        self.fase.atualizar(self.jogador)
        self.camera.atualizar(self.jogador)
        self.camera.remover_fora_da_tela(self.tiros_jogador)

        pontos = tiros_do_jogador_x_inimigos(self.tiros_jogador, self.fase.inimigos)
        if pontos > 0:                 # só ganha pontos quando um inimigo morre
            self.pontos += pontos
            self.som.tocar("inimigo_morre")
        if self.jogador.esta_vivo():
            if inimigos_x_jogador(self.jogador, self.fase.inimigos, self.fase.tiros_inimigos):
                self.som.tocar("dano")

        self.verificar_fim()

    def verificar_fim(self):
        """Troca de estado quando o jogador morre ou chega ao fim da fase."""
        agora = pygame.time.get_ticks()
        if not self.jogador.esta_vivo():
            if self.morreu_em is None:
                self.morreu_em = agora
            elif agora - self.morreu_em > ESPERA_GAME_OVER:
                self.mudar_estado("game_over")
        elif self.fase.terminou(self.jogador):
            if existe_fase(self.numero_fase + 1):
                self.carregar_fase(self.numero_fase + 1)
            else:
                self.mudar_estado("vitoria")

    # ------------------------------------------------------------ desenho
    def desenhar(self):
        """Desenha a tela do estado atual."""
        if self.estado == "jogando":
            self.fase.desenhar(self.tela, self.camera)
            self.camera.desenhar_grupo(self.tela, self.tiros_jogador)
            self.tela.blit(self.jogador.image, self.camera.aplicar(self.jogador.rect))
            self.hud.desenhar(self.tela, self.jogador.vida, self.pontos, self.numero_fase)  # por último: fica por cima
        elif self.estado == "inicio":
            self.telas.desenhar_inicio(self.tela)
        elif self.estado == "game_over":
            self.telas.desenhar_game_over(self.tela, self.pontos)
        elif self.estado == "vitoria":
            self.telas.desenhar_vitoria(self.tela, self.pontos)


if __name__ == "__main__":
    Jogo().rodar()
