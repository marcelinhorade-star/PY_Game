"""Placar (ranking) das maiores pontuações, salvo no arquivo placar.json.

O arquivo fica na pasta do jogo e guarda uma lista de dicionários, por exemplo:
    [{"nome": "MARCELO", "pontos": 1200, "personagem": "Vespa"}, ...]

Se o arquivo não existir (primeira vez que o jogo roda) ou estiver estragado,
o placar começa vazio em vez de o jogo travar.
"""
import json
import os

import config

ARQUIVO_PLACAR = os.path.join(config.PASTA_JOGO, "placar.json")
TAMANHO_PLACAR = 10   # quantas pontuações o placar guarda e mostra
TAMANHO_NOME = 12     # máximo de letras do nome digitado


def carregar_placar():
    """Lê o placar do arquivo e devolve a lista, da maior para a menor pontuação.

    Devolve [] se o arquivo não existe ou não é um JSON válido.
    """
    try:
        with open(ARQUIVO_PLACAR, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, ValueError):   # OSError: não existe; ValueError: JSON quebrado
        return []
    if not isinstance(dados, list):
        return []
    # ignora linhas estranhas (alguém editou o arquivo à mão, por exemplo)
    placar = [linha for linha in dados
              if isinstance(linha, dict)
              and isinstance(linha.get("nome"), str)
              and isinstance(linha.get("pontos"), int)]
    placar.sort(key=lambda linha: linha["pontos"], reverse=True)
    return placar[:TAMANHO_PLACAR]


def salvar_pontuacao(nome, pontos, personagem):
    """Coloca a pontuação no placar, grava o arquivo e devolve (placar, posicao).

    posicao é o índice (0 = primeiro lugar) da pontuação nova no placar,
    ou None se ela não foi alta o bastante para entrar no top 10.
    """
    nova = {"nome": nome, "pontos": pontos, "personagem": personagem}
    placar = carregar_placar()
    placar.append(nova)
    # sort é "estável": num empate, quem já estava no placar continua na frente
    placar.sort(key=lambda linha: linha["pontos"], reverse=True)
    placar = placar[:TAMANHO_PLACAR]
    try:
        with open(ARQUIVO_PLACAR, "w", encoding="utf-8") as arquivo:
            json.dump(placar, arquivo, ensure_ascii=False, indent=2)
    except OSError:
        pass   # sem permissão para gravar: o placar só vale até fechar o jogo
    # "is" compara o objeto em si (não o conteúdo), achando exatamente a linha nova
    for i, linha in enumerate(placar):
        if linha is nova:
            return placar, i
    return placar, None
