"""Funções de colisão entre jogador, inimigos, tiros e plataformas."""
import pygame


def altura_do_chao(rect, plataformas, sem_chao=10000):
    """Devolve a altura (y) da superfície mais alta logo abaixo dos pés de rect.

    Só conta plataformas que estão sob o rect no eixo x e cujo topo está na
    altura dos pés ou abaixo deles. Sem nenhuma (buraco), devolve sem_chao e o
    personagem cai.
    """
    chao = sem_chao
    for plataforma in plataformas:
        em_cima = plataforma.rect.left < rect.right and plataforma.rect.right > rect.left
        abaixo_dos_pes = plataforma.rect.top >= rect.bottom
        if em_cima and abaixo_dos_pes and plataforma.rect.top < chao:
            chao = plataforma.rect.top
    return chao


def tiros_do_jogador_x_inimigos(tiros_jogador, inimigos):
    """Tira vida dos inimigos atingidos e devolve os pontos ganhos neste quadro.

    groupcollide devolve {inimigo: [tiros que acertaram]}. O False mantém o
    inimigo no grupo (ele só some quando a vida acaba) e o True apaga os tiros.
    """
    pontos = 0
    acertos = pygame.sprite.groupcollide(inimigos, tiros_jogador, False, True)
    for inimigo, tiros in acertos.items():
        if inimigo.levar_dano(len(tiros)):
            pontos += inimigo.PONTOS
    return pontos


def inimigos_x_jogador(jogador, inimigos, tiros_inimigos):
    """Dá dano no jogador se um tiro inimigo acertar ou se ele encostar num inimigo.

    Os tiros que acertam somem. Retorna True se o jogador perdeu vida.
    """
    tiros = pygame.sprite.spritecollide(jogador, tiros_inimigos, True)
    encostou = pygame.sprite.spritecollide(jogador, inimigos, False)
    if tiros or encostou:
        return jogador.levar_dano()
    return False
