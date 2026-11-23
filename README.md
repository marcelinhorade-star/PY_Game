# Linha de Fogo

Jogo de tiro com rolagem lateral (no estilo *run and gun*) feito em Python com
pygame-ce para o Projeto Final de **Design de Software** (Insper, 2026.2).

Atravesse as fases atirando nos soldados inimigos, desvie dos tiros e dos
foguetes e passe pelas 3 fases sem perder todas as vidas. No fim da fase 3
você enfrenta o chefe, o Comandante: só dá para vencer o jogo derrotando ele.

## Como jogar

- **Escolha um personagem** antes de começar. Cada um tem vida, velocidade e arma diferentes:

  | Personagem | Vida | Velocidade | Arma |
  |---|---|---|---|
  | Recruta | 5 | média | Pistola: tiro rápido e de longo alcance |
  | Brutus | 7 | lenta | Canhão: tiro lento que tira 3 de vida |
  | Vespa | 3 | rápida | Escopeta: 3 balas em leque, alcance curto |

- **Mate todos os inimigos para avançar.** Uma parede invisível não deixa você
  passar muito à frente do último inimigo vivo, inclusive os que estão em cima
  das plataformas (use o tiro na diagonal para acertá-los do chão).
- **Cuidado com os buracos no chão.** Quem cai perde 1 vida e volta para o último
  chão firme. Alguns buracos só dá para atravessar pulando pelas plataformas, e
  na fase 2 há uma plataforma que se mexe e leva você para o outro lado.
- **Placar:** no fim da partida você digita seu nome e a pontuação é salva no
  placar das maiores pontuações (arquivo `placar.json`).

## Integrantes

| Integrante | Parte do projeto |
|---|---|
| Marcelo (`marcelinhorade-star`) | Jogador, personagens, tiro e chefe: `jogador.py`, `personagens.py`, `tiro.py`, `chefe.py` |
| Gabriel Gonçalves (`Gabriel2763`) | Inimigos, colisões, câmera, cenário e fases: `inimigo.py`, `colisoes.py`, `camera.py`, `cenario.py`, `efeitos.py`, `fase.py` |
| Victor Kim (`victortykim`) | Loop principal, telas, HUD, som e README: `main.py`, `config.py`, `telas.py`, `hud.py`, `som.py` |

## Vídeo

[Assista ao vídeo do jogo no YouTube](https://youtu.be/nEh-VetZ4NQ)

## Como instalar e rodar

1. Instale o Python 3.10 ou mais novo.
2. Instale a biblioteca do jogo:

   ```
   pip install pygame-ce
   ```

3. Na pasta do projeto, rode:

   ```
   python main.py
   ```

## Controles

| Tecla | Ação |
|---|---|
| Setas esquerda / direita | andar (na tela de escolha: trocar de personagem) |
| Seta para cima | mirar para cima |
| Seta para cima + esquerda ou direita | mirar na diagonal |
| Seta para baixo | agachar |
| Espaço | pular |
| Z | atirar (segure para atirar sem parar) |
| P ou ESC | pausar / continuar |
| Q (com o jogo pausado) | desistir da partida e voltar ao menu |
| ENTER | começar / escolher o personagem / confirmar o nome / jogar de novo |
| Letras e BACKSPACE | digitar e apagar o nome no fim da partida |

## Como o código está organizado

O jogo é orientado a objetos e cada arquivo cuida de uma parte:

- `main.py`: classe `Jogo`, com o loop principal e a máquina de estados
  (`inicio` → `escolha` → `jogando` → `nome` → `game_over` ou `vitoria` → `inicio`,
  e `jogando` ↔ `pausa` com P ou ESC).
- `config.py`: constantes compartilhadas (tamanho da tela, FPS, cores, pastas).
- `telas.py`: telas de início, escolha de personagem, pausa, nome, game over e vitória.
- `placar.py`: salva e lê o placar das maiores pontuações (`placar.json`).
- `hud.py`: vida, fase e pontuação durante o jogo.
- `som.py`: música de fundo e efeitos sonoros.
- `jogador.py` / `tiro.py`: o personagem, suas animações, as 3 armas e os tiros.
- `personagens.py`: os 3 personagens que dá para escolher (vida, velocidade, arma e cor).
- `fase.py`, `cenario.py`, `camera.py`, `inimigo.py`, `efeitos.py`, `colisoes.py`:
  mapas das fases (com buracos e plataforma móvel), fundo com paralaxe, câmera,
  inimigos, explosões e colisões.
- `chefe.py`: o chefe da fase 3 (soldado gigante com barra de vida e 2 ataques).

## Créditos

**Imagens:** todas as imagens do jogo (jogador, inimigos, chefe, tiros, explosões,
cenários e plataformas) vêm do pacote
[Generic RUN n' GUN](https://bakudas.itch.io/generic-run-n-gun), de Vaca Roxa
(arte de @Anokolisa e @al_MSantos), licença CC0. A bala e o clarão do tiro foram
recortados das folhas de sprites do próprio pacote.

**Sons e músicas:** Juhani Junkala (SubspaceAudio), licença CC0, baixados do OpenGameArt:

- [512 Sound Effects (8-bit style)](https://opengameart.org/content/512-sound-effects-8-bit-style):
  `tiro.wav` (sfx_wpn_machinegun_loop1), `dano.wav` (sfx_sounds_damage1),
  `inimigo_morre.wav` (sfx_deathscream_human1), `game_over.wav` (sfx_sounds_negative1),
  `vitoria.wav` (sfx_sounds_fanfare1).
- [5 Chiptunes (Action)](https://opengameart.org/content/5-chiptunes-action):
  `musica_menu.wav` (Title Screen) e `musica_fase.wav` (Level 1). As músicas foram
  convertidas para mono e 22 kHz para deixar o repositório menor.

## Uso de Inteligência Artificial

Usamos IA generativa no projeto, como permite a política da disciplina:

- **Claude (Anthropic)**: usado pelo Victor para escrever, passo a passo e com
  explicações, a primeira versão de `config.py`, `main.py`, `telas.py`, `hud.py`
  e `som.py`, para escolher e converter os sons e para escrever este README.
  Tudo foi revisado e testado pelo grupo. Chat: https://claude.ai/share/5c09a0a7-1d5d-4425-89dc-f31f8f3e1eba
- **Claude (Anthropic)**: usado pelo Marcelo para escrever, passo a passo e com
  explicações, `jogador.py`, `tiro.py`, `personagens.py` e `chefe.py`, e para
  recortar as imagens do jogador e do tiro do pacote de sprites. Também foi usado
  para balancear o jogo (números dos inimigos em `inimigo.py`, buracos no chão,
  plataforma móvel e parede invisível em `fase.py`, tiro na diagonal), testando
  cada mudança com simulações do jogo. Tudo foi revisado e testado pelo grupo.
  Conversas: [projeto no Claude](https://claude.ai/code/project/chan_014E4dHx1o6LGTzQDRm4Mp3G).
- **Claude (Anthropic)**: usado pelo Gabriel para escrever, passo a passo e com
  explicações, `fase.py`, `colisoes.py`, `camera.py`, `inimigo.py`, `efeitos.py` e
  `cenario.py` (cerca de 100% gerados por IA, seguindo o padrão do handout de PyGame),
  para baixar o pacote de sprites e recortar os quadros dos inimigos e do cenário, e
  para testar cada etapa com simulações automáticas do jogo. O Gabriel testou e
  validou cada arquivo e fez os commits. Conversa completa no anexo:
  [anexos/chat_pessoa_B.md](anexos/chat_pessoa_B.md).
