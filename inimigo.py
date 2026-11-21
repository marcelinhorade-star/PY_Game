"""Inimigos do jogo: o soldado (Inimigo), o Drone, os tiros inimigos e a explosão."""
import math
import pygame
from colisoes import altura_do_chao
from jogador import criar_frames_provisorios


def criar_frames_drone(quantidade, cor_luz):
    """Desenha o drone provisório: corpo cinza e hélice que muda de tamanho a cada frame."""
    frames = []
    for i in range(quantidade):
        frame = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.rect(frame, (90, 90, 110), (5, 10, 40, 16))   # corpo
        pygame.draw.rect(frame, cor_luz, (38, 14, 5, 5))          # luz (frente)
        helice = 40 if i % 2 == 0 else 16
        pygame.draw.line(frame, (30, 30, 30), (25 - helice // 2, 4), (25 + helice // 2, 4), 3)
        frames.append(frame)
    return frames


def criar_frames_explosao(quantidade=6):
    """Desenha a explosão provisória: um círculo que cresce e vai sumindo."""
    frames = []
    for i in range(quantidade):
        raio = 8 + i * 6
        frame = pygame.Surface((2 * raio, 2 * raio), pygame.SRCALPHA)
        pygame.draw.circle(frame, (255, 160 - i * 20, 0, 255 - i * 35), (raio, raio), raio)
        frames.append(frame)
    return frames


def carregar_assets_inimigos():
    """Cria UMA vez as animações de todos os inimigos e da explosão.

    Os inimigos recebem este dicionário pronto, em vez de cada um carregar as
    próprias imagens (mesma ideia do dicionário assets do handout).
    """
    return {
        "soldado": {
            "andando": criar_frames_provisorios((180, 40, 40), 4),
            "atirando": criar_frames_provisorios((255, 120, 40), 2),
        },
        "drone": {
            "andando": criar_frames_drone(4, (255, 60, 60)),
            "atirando": criar_frames_drone(2, (255, 230, 0)),
        },
        "explosao": criar_frames_explosao(),
    }


class TiroInimigo(pygame.sprite.Sprite):
    """Projétil dos inimigos; some depois de percorrer uma certa distância."""

    def __init__(self, x, y, vel_x, vel_y):
        """Cria o tiro com centro em (x, y) e velocidade (vel_x, vel_y)."""
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 70, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.percorrido = 0
        self.alcance = 600

    def update(self):
        """Move o tiro e apaga quando ele passa do alcance."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.percorrido += abs(self.vel_x) + abs(self.vel_y)
        if self.percorrido > self.alcance:
            self.kill()


class Explosao(pygame.sprite.Sprite):
    """Animação que toca uma vez no lugar onde um inimigo morreu."""

    def __init__(self, centro, frames):
        """Cria a explosão centrada em centro, usando a lista de frames."""
        super().__init__()
        self.frames = frames
        self.frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=centro)
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 60

    def update(self):
        """Avança um frame a cada frame_ticks ms e some no fim da animação."""
        agora = pygame.time.get_ticks()
        if agora - self.last_update > self.frame_ticks:
            self.last_update = agora
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill()
            else:
                centro = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect(center=centro)


class Inimigo(pygame.sprite.Sprite):
    """Soldado que patrulha, persegue o jogador quando ele chega perto e atira."""

    NOME = "soldado"            # chave das animações em assets
    VIDA = 3
    VELOCIDADE = 1
    PONTOS = 100
    DISTANCIA_VISAO = 300       # a partir daqui ele vê o jogador
    DISTANCIA_MINIMA = 150      # para de chegar perto e só atira
    RAIO_PATRULHA = 100

    def __init__(self, x, y, assets, grupos):
        """Cria o inimigo com os pés em (x, y).

        assets: dicionário de carregar_assets_inimigos().
        grupos: dicionário com os grupos "tiros_inimigos" e "efeitos".
        """
        super().__init__()
        self.assets = assets
        self.grupos = grupos
        self.animacoes = assets[self.NOME]
        self.estado = "andando"
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 150
        self.image = self.animacoes["andando"][0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.x_inicial = x
        self.vida = self.VIDA
        self.direcao = -1
        self.vel_y = 0
        self.ultimo_tiro = pygame.time.get_ticks()
        self.shoot_ticks = 1500

    def distancia_ate(self, jogador):
        """Distância horizontal (em pixels) até o jogador."""
        return abs(jogador.rect.centerx - self.rect.centerx)

    def tem_chao_a_frente(self, plataformas):
        """True se o próximo passo ainda tem chão (para não cair da plataforma)."""
        frente = self.rect.move(self.direcao * self.rect.width, 0)
        return altura_do_chao(frente, plataformas) == self.rect.bottom

    def mover(self, jogador, plataformas):
        """Persegue o jogador se ele estiver perto; senão, patrulha."""
        if self.distancia_ate(jogador) < self.DISTANCIA_VISAO:
            self.direcao = 1 if jogador.rect.centerx > self.rect.centerx else -1
            longe = self.distancia_ate(jogador) > self.DISTANCIA_MINIMA
            if longe and self.tem_chao_a_frente(plataformas):
                self.rect.x += self.VELOCIDADE * 2 * self.direcao
        else:
            saiu_da_area = abs(self.rect.centerx - self.x_inicial) > self.RAIO_PATRULHA
            voltando = (self.x_inicial - self.rect.centerx) * self.direcao > 0
            if (saiu_da_area and not voltando) or not self.tem_chao_a_frente(plataformas):
                self.direcao *= -1
            self.rect.x += self.VELOCIDADE * self.direcao

    def aplicar_gravidade(self, plataformas):
        """Puxa o inimigo para baixo até a plataforma embaixo dele."""
        chao = altura_do_chao(self.rect, plataformas)
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= chao:
            self.rect.bottom = chao
            self.vel_y = 0

    def criar_tiro(self):
        """Cria o tiro do soldado: reto, na direção em que ele olha."""
        return TiroInimigo(self.rect.centerx, self.rect.centery - 8, 6 * self.direcao, 0)

    def atirar(self, jogador):
        """Atira de shoot_ticks em shoot_ticks ms enquanto vê o jogador."""
        agora = pygame.time.get_ticks()
        if self.distancia_ate(jogador) < self.DISTANCIA_VISAO and agora - self.ultimo_tiro > self.shoot_ticks:
            self.grupos["tiros_inimigos"].add(self.criar_tiro())
            self.ultimo_tiro = agora

    def animar(self):
        """Escolhe a animação (andando ou atirando) e troca de frame com o tempo."""
        agora = pygame.time.get_ticks()
        novo = "atirando" if agora - self.ultimo_tiro < 250 else "andando"
        if novo != self.estado:
            self.estado = novo
            self.frame = 0
        frames = self.animacoes[self.estado]
        if agora - self.last_update > self.frame_ticks:
            self.last_update = agora
            self.frame = (self.frame + 1) % len(frames)
        imagem = frames[self.frame % len(frames)]
        if self.direcao == -1:
            imagem = pygame.transform.flip(imagem, True, False)
        self.image = imagem
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def levar_dano(self, quantidade=1):
        """Tira vida. Se zerar, cria a explosão, some e retorna True."""
        self.vida -= quantidade
        if self.vida <= 0:
            self.grupos["efeitos"].add(Explosao(self.rect.center, self.assets["explosao"]))
            self.kill()
            return True
        return False

    def update(self, jogador, plataformas):
        """Atualiza o inimigo uma vez por quadro."""
        self.mover(jogador, plataformas)
        self.aplicar_gravidade(plataformas)
        self.atirar(jogador)
        self.animar()


class Drone(Inimigo):
    """Inimigo voador: fica sobre o jogador e solta bombas para baixo.

    Herda tudo do Inimigo e só muda o que é diferente.
    """

    NOME = "drone"
    VIDA = 2
    VELOCIDADE = 2
    PONTOS = 150
    DISTANCIA_MINIMA = 10

    def __init__(self, x, y, assets, grupos):
        """Cria o drone voando com a base em (x, y)."""
        super().__init__(x, y, assets, grupos)
        self.y_base = y
        self.shoot_ticks = 1200

    def tem_chao_a_frente(self, plataformas):
        """Drones voam, então sempre podem seguir em frente."""
        return True

    def aplicar_gravidade(self, plataformas):
        """Drones não caem: só balançam para cima e para baixo."""
        self.rect.bottom = self.y_base + int(8 * math.sin(pygame.time.get_ticks() / 300))

    def criar_tiro(self):
        """Cria a bomba do drone, que cai reto para baixo."""
        return TiroInimigo(self.rect.centerx, self.rect.bottom, 0, 5)
