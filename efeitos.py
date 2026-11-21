"""Tiros dos inimigos e animações que tocam uma vez só (morte, explosão)."""
import pygame


class TiroInimigo(pygame.sprite.Sprite):
    """Projétil dos inimigos; some depois de percorrer uma certa distância."""

    def __init__(self, imagem, x, y, vel_x, vel_y):
        """Cria o tiro com centro em (x, y) e velocidade (vel_x, vel_y)."""
        super().__init__()
        self.image = imagem
        if vel_x < 0:
            self.image = pygame.transform.flip(imagem, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.percorrido = 0
        self.alcance = 700

    def update(self):
        """Move o tiro e apaga quando ele passa do alcance."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.percorrido += abs(self.vel_x) + abs(self.vel_y)
        if self.percorrido > self.alcance:
            self.kill()

    def ao_acertar(self):
        """Chamado quando o tiro bate em algo. O tiro comum só some."""
        self.kill()


class Foguete(TiroInimigo):
    """Tiro da bazuca: mais lento e explode quando bate em algo."""

    def __init__(self, imagem, x, y, vel_x, frames_explosao, grupo_efeitos):
        """Cria o foguete; guarda o que precisa para explodir depois."""
        super().__init__(imagem, x, y, vel_x, 0)
        self.frames_explosao = frames_explosao
        self.grupo_efeitos = grupo_efeitos

    def ao_acertar(self):
        """Cria uma explosão no lugar do impacto e some."""
        self.grupo_efeitos.add(Efeito(self.frames_explosao, midbottom=self.rect.midbottom))
        self.kill()


class Efeito(pygame.sprite.Sprite):
    """Animação que toca uma vez e some (corpo caindo, explosão...).

    É a mesma ideia da classe Explosion do handout: troca de frame a cada
    frame_ticks ms e chama kill() depois do último.
    """

    def __init__(self, frames, midbottom, frame_ticks=90):
        """Cria o efeito com a base (pés) em midbottom."""
        super().__init__()
        self.frames = frames
        self.frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = frame_ticks

    def update(self):
        """Avança um frame a cada frame_ticks ms e some no fim da animação."""
        agora = pygame.time.get_ticks()
        if agora - self.last_update > self.frame_ticks:
            self.last_update = agora
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill()
            else:
                base = self.rect.midbottom
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect(midbottom=base)
