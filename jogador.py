"""Jogador controlado pelo usuário (Pessoa A).

Define a classe Jogador, que anda, pula, agacha, mira para cima, atira,
leva dano (com invencibilidade e piscar) e troca de animação conforme o
estado. Também tem as funções que carregam os frames do pacote de sprites
"Generic RUN n' GUN" (CC0), com retângulos provisórios caso as imagens
não existam.
"""
import os
import pygame
from tiro import Tiro, Clarao

# Pasta com os frames do jogador, sempre ao lado deste arquivo
# (funciona não importa de qual pasta o jogo for rodado).
PASTA_IMAGENS = os.path.join(os.path.dirname(__file__), "imagens", "jogador")

# Os frames originais são pequenos (pixel art), então aumentamos 2 vezes.
ESCALA = 2

# Quantos frames cada animação tem. Os arquivos se chamam nome_0.png, nome_1.png...
QUANTIDADE_FRAMES = {
    "parado": 6,
    "andando": 8,
    "pulando": 2,
    "agachado": 1,
    "mirando_cima": 1,
    "andando_cima": 8,
    "morrendo": 5,
}


def criar_frames_provisorios(cor, quantidade, altura=60):
    """Cria frames simples (retângulo com pernas), usados se as imagens não existirem."""
    frames = []
    for i in range(quantidade):
        frame = pygame.Surface((40, altura), pygame.SRCALPHA)
        corpo = altura - 15
        pygame.draw.rect(frame, cor, (5, 0, 30, corpo))           # corpo
        pygame.draw.rect(frame, (255, 255, 255), (28, 10, 6, 6))  # olho
        passo = 8 if i % 2 == 0 else -8
        pygame.draw.line(frame, cor, (20, corpo), (20 + passo, altura), 5)
        pygame.draw.line(frame, cor, (20, corpo), (20 - passo, altura), 5)
        frames.append(frame)
    return frames


def carregar_frames(nome, quantidade):
    """Carrega os arquivos nome_0.png ... nome_N.png e aumenta cada um pela ESCALA."""
    frames = []
    for i in range(quantidade):
        caminho = os.path.join(PASTA_IMAGENS, f"{nome}_{i}.png")
        imagem = pygame.image.load(caminho)
        if pygame.display.get_surface() is not None:
            imagem = imagem.convert_alpha()  # deixa o desenho mais rápido
        imagem = pygame.transform.scale_by(imagem, ESCALA)
        frames.append(imagem)
    return frames


def carregar_animacoes():
    """Monta o dicionário {estado: lista de frames}.

    Se a pasta de imagens não existir, usa os retângulos provisórios.
    """
    if not os.path.isdir(PASTA_IMAGENS):
        azul = (0, 120, 255)
        return {
            "parado": criar_frames_provisorios(azul, 1),
            "andando": criar_frames_provisorios(azul, 4),
            "pulando": criar_frames_provisorios((0, 80, 200), 1),
            "agachado": criar_frames_provisorios(azul, 1, altura=40),
            "mirando_cima": criar_frames_provisorios(azul, 1),
            "andando_cima": criar_frames_provisorios(azul, 4),
            # deitado: o mesmo boneco girado 90 graus
            "morrendo": [pygame.transform.rotate(criar_frames_provisorios(azul, 1)[0], 90)],
        }
    animacoes = {}
    for nome, quantidade in QUANTIDADE_FRAMES.items():
        animacoes[nome] = carregar_frames(nome, quantidade)
    return animacoes


class Jogador(pygame.sprite.Sprite):
    """Personagem controlado pelo jogador."""

    def __init__(self, x, y):
        """Cria o jogador na posição (x, y), que é o ponto entre os pés."""
        super().__init__()
        self.animacoes = carregar_animacoes()
        self.estado = "parado"
        self.frame_atual = 0
        self.ultimo_frame = 0
        self.image = self.animacoes["parado"][0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel_y = 0
        self.no_chao = True
        self.vida = 5               # era 3 (agora é preciso matar todos os inimigos)
        self.direcao = 1  # 1 = direita, -1 = esquerda
        self.ultimo_tiro = 0
        self.ultimo_dano = -10000   # momento (ms) do último dano
        self.invencivel_ms = 1000   # tempo de invencibilidade após dano
        self.agachado = False       # seta para baixo
        self.mirando_cima = False   # seta para cima

    def ler_mira(self, teclas):
        """Vê se o jogador está agachado ou mirando para cima."""
        self.agachado = teclas[pygame.K_DOWN] and self.no_chao
        self.mirando_cima = teclas[pygame.K_UP] and not self.agachado

    def mover(self, teclas):
        """Anda para os lados com as setas (mais devagar agachado)."""
        velocidade = 2 if self.agachado else 5
        if teclas[pygame.K_LEFT]:
            self.rect.x -= velocidade
            self.direcao = -1
        if teclas[pygame.K_RIGHT]:
            self.rect.x += velocidade
            self.direcao = 1

    def pular(self):
        """Pula se estiver no chão, não estiver agachado e estiver vivo."""
        if self.no_chao and not self.agachado and self.esta_vivo():
            self.vel_y = -15
            self.no_chao = False

    def ponta_da_arma(self):
        """Retorna (x, y, para_cima): onde fica a ponta da arma agora."""
        if self.mirando_cima:
            # a imagem tem 10 px vazios em cima, então a arma começa em top + 10
            return self.rect.centerx - 5 * self.direcao, self.rect.top + 10, True
        return self.rect.centerx + 20 * self.direcao, self.rect.top + 23, False

    def atirar(self, grupo_tiros):
        """Cria um tiro e um clarão na ponta da arma, com intervalo de 250 ms."""
        if not self.esta_vivo():
            return  # morto não atira
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > 250:
            x, y, para_cima = self.ponta_da_arma()
            tiro = Tiro(x, y, self.direcao, para_cima=para_cima)
            grupo_tiros.add(tiro)
            grupo_tiros.add(Clarao(self))
            self.ultimo_tiro = agora

    def aplicar_gravidade(self, chao_y):
        """Puxa o jogador para baixo até o chão.

        chao_y é a altura da superfície logo abaixo dos pés (o chão ou uma
        plataforma), calculada por colisoes.altura_do_chao.
        """
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self.vel_y = 0
            self.no_chao = True
        else:
            # saiu da beirada de uma plataforma ou está no ar
            self.no_chao = False

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
        andando = teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]
        if not self.esta_vivo():
            novo = "morrendo"
        elif not self.no_chao:
            novo = "pulando"
        elif self.agachado:
            novo = "agachado"
        elif self.mirando_cima and andando:
            novo = "andando_cima"
        elif self.mirando_cima:
            novo = "mirando_cima"
        elif andando:
            novo = "andando"
        else:
            novo = "parado"
        if novo != self.estado:
            self.estado = novo
            self.frame_atual = 0

    def animar(self):
        """Troca de frame a cada 100 ms e vira a imagem para a direção certa.

        As animações repetem em loop, menos a de morte, que para no último
        frame (o jogador fica deitado no chão).
        """
        agora = pygame.time.get_ticks()
        frames = self.animacoes[self.estado]
        if agora - self.ultimo_frame > 100:
            if self.estado == "morrendo":
                self.frame_atual = min(self.frame_atual + 1, len(frames) - 1)
            else:
                self.frame_atual = (self.frame_atual + 1) % len(frames)
            self.ultimo_frame = agora
        imagem = frames[self.frame_atual]
        if self.direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        self.image = imagem
        # cada animação tem um tamanho: refaz o rect mantendo os pés no lugar
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def piscar(self):
        """Faz o jogador piscar enquanto está invencível (morto não pisca)."""
        if self.esta_invencivel() and self.esta_vivo():
            visivel = (pygame.time.get_ticks() // 100) % 2 == 0
            # copia para não deixar o frame original transparente para sempre
            self.image = self.image.copy()
            self.image.set_alpha(255 if visivel else 80)

    def update(self, teclas, chao_y):
        """Atualiza o jogador a cada quadro.

        Morto, ele ignora as teclas: só cai (gravidade) e anima a morte.
        """
        if self.esta_vivo():
            self.ler_mira(teclas)
            self.mover(teclas)
        else:
            self.agachado = False
            self.mirando_cima = False
        self.aplicar_gravidade(chao_y)
        self.atualizar_estado(teclas)
        self.animar()
        self.piscar()
