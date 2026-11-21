"""Funções de colisão entre jogador, inimigos, tiros e plataformas."""


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
