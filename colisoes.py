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
    collide_mask compara os pixels desenhados, e não o retângulo inteiro, então
    tiro que passa na parte transparente da imagem não conta.
    """
    pontos = 0
    acertos = pygame.sprite.groupcollide(inimigos, tiros_jogador, False, True,
                                         pygame.sprite.collide_mask)
    for inimigo, tiros in acertos.items():
        if inimigo.levar_dano(len(tiros)):
            pontos += inimigo.PONTOS
    return pontos


def inimigos_x_jogador(jogador, inimigos, tiros_inimigos):
    """Dá dano no jogador se um tiro inimigo acertar ou se ele encostar num inimigo.

    Cada tiro que acerta chama ao_acertar() (o foguete explode, o tiro comum
    só some). Retorna True se o jogador perdeu vida.
    """
    tiros = pygame.sprite.spritecollide(jogador, tiros_inimigos, False, pygame.sprite.collide_mask)
    for tiro in tiros:
        tiro.ao_acertar()
    encostou = pygame.sprite.spritecollide(jogador, inimigos, False, pygame.sprite.collide_mask)
    if tiros or encostou:
        return jogador.levar_dano()
    return False


def tiros_inimigos_x_plataformas(tiros_inimigos, plataformas):
    """Faz os tiros inimigos pararem quando batem no chão ou numa plataforma."""
    acertos = pygame.sprite.groupcollide(tiros_inimigos, plataformas, False, False)
    for tiro in acertos:
        tiro.ao_acertar()
