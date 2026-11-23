"""Os 3 personagens que o jogador pode escolher antes da partida (Pessoa A).

Cada personagem é um dicionário com:
    nome:        nome mostrado na tela de escolha
    descricao:   frase curta mostrada embaixo do nome
    vida:        vida inicial (e máxima) = quantos corações aparecem no HUD
    velocidade:  pixels por quadro quando anda
    arma:        chave do dicionário ARMAS, em tiro.py
    troca_cor:   ordem dos canais (R, G, B) usada para pintar a roupa azul
                 de outra cor; None = cores originais do sprite

Todos usam os mesmos desenhos (pacote "Generic RUN n' GUN", CC0); o que muda
o visual é a troca de cor da roupa (ver trocar_cor em jogador.py).
"""

PERSONAGENS = [
    {
        "nome": "Recruta",
        "descricao": "Equilibrado. Pistola rápida e de longo alcance.",
        "vida": 5,
        "velocidade": 5,
        "arma": "pistola",
        "troca_cor": None,          # roupa azul (original)
    },
    {
        "nome": "Brutus",
        "descricao": "Muita vida e lento. Canhão: tiro lento que tira 3 de vida.",
        "vida": 7,
        "velocidade": 4,
        "arma": "canhao",
        "troca_cor": (2, 0, 0),     # (R, G, B) vira (B, R, R): roupa vermelha
    },
    {
        "nome": "Vespa",
        "descricao": "Pouca vida e rápida. Escopeta: 3 balas em leque, curto alcance.",
        "vida": 3,
        "velocidade": 7,
        "arma": "escopeta",
        "troca_cor": (0, 2, 0),     # (R, G, B) vira (R, B, R): roupa verde
    },
]
