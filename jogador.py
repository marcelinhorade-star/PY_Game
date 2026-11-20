import pygame
from tiro import Tiro


def criar_frames_provisorios(cor, quantidade):
    """Cria frames simples (retângulo com pernas) só para testar a animação."""
    frames = []
    for i in range(quantidade):
        frame = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.rect(frame, cor, (5, 0, 30, 45))              # corpo
        pygame.draw.rect(frame, (255, 255, 255), (28, 10, 6, 6))  # olho
        passo = 8 if i % 2 == 0 else -8
        pygame.draw.line(frame, cor, (20, 45), (20 + passo, 60), 5)  # perna 1
        pygame.draw.line(frame, cor, (20, 45), (20 - passo, 60), 5)  # perna 2
        frames.append(frame)
    return frames


class Jogador(pygame.sprite.Sprite):
    """Personagem controlado pelo jogador."""

    def __init__(self, x, y):
        """Cria o jogador na posição (x, y)."""
        super().__init__()
        self.animacoes = {
            "parado": criar_frames_provisorios((0, 120, 255), 1),
            "andando": criar_frames_provisorios((0, 120, 255), 4),
            "pulando": criar_frames_provisorios((0, 80, 200), 1),
        }
        self.estado = "parado"
        self.frame_atual = 0
        self.ultimo_frame = 0
        self.image = self.animacoes["parado"][0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel_y = 0
        self.no_chao = True
        self.vida = 3
        self.direcao = 1  # 1 = direita, -1 = esquerda
        self.ultimo_tiro = 0
        self.ultimo_dano = -10000   # momento (ms) do último dano
        self.invencivel_ms = 1000   # tempo de invencibilidade após dano

    def mover(self, teclas):
        """Anda para os lados com as setas."""
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
            self.direcao = -1
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
            self.direcao = 1

    def pular(self):
        """Pula se estiver no chão."""
        if self.no_chao:
            self.vel_y = -15
            self.no_chao = False

    def atirar(self, grupo_tiros):
        """Cria um tiro, com intervalo de 250 ms entre tiros."""
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > 250:
            tiro = Tiro(self.rect.centerx, self.rect.centery, self.direcao)
            grupo_tiros.add(tiro)
            self.ultimo_tiro = agora

    def aplicar_gravidade(self, chao_y):
        """Puxa o jogador para baixo até o chão."""
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self.vel_y = 0
            self.no_chao = True

    def esta_invencivel(self):
        """Retorna True se o jogador levou dano há pouco tempo."""
        return pygame.time.get_ticks() - self.ultimo_dano < self.invencivel_ms

    def levar_dano(self, quantidade=1):
        """Tira vida do jogador, se ele não estiver invencível.

        Retorna True se o dano foi aplicado, False se foi ignorado.
        """
        if self.esta_invencivel():
            return False
        self.vida -= quantidade
        if self.vida < 0:
            self.vida = 0
        self.ultimo_dano = pygame.time.get_ticks()
        return True

    def esta_vivo(self):
        """Retorna True enquanto o jogador tiver vida."""
        return self.vida > 0

    def atualizar_estado(self, teclas):
        """Escolhe a animação conforme o que o jogador está fazendo."""
        if not self.no_chao:
            novo = "pulando"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            novo = "andando"
        else:
            novo = "parado"
        if novo != self.estado:
            self.estado = novo
            self.frame_atual = 0

    def animar(self):
        """Troca de frame a cada 100 ms e vira a imagem para a direção certa."""
        agora = pygame.time.get_ticks()
        frames = self.animacoes[self.estado]
        if agora - self.ultimo_frame > 100:
            self.frame_atual = (self.frame_atual + 1) % len(frames)
            self.ultimo_frame = agora
        imagem = frames[self.frame_atual]
        if self.direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        self.image = imagem

    def piscar(self):
        """Faz o jogador piscar enquanto está invencível."""
        if self.esta_invencivel():
            visivel = (pygame.time.get_ticks() // 100) % 2 == 0
            self.image.set_alpha(255 if visivel else 80)
        else:
            self.image.set_alpha(255)

    def update(self, teclas, chao_y):
        """Atualiza o jogador a cada quadro."""
        self.mover(teclas)
        self.aplicar_gravidade(chao_y)
        self.atualizar_estado(teclas)
        self.animar()
        self.piscar()