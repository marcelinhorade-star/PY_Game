# Linha de Fogo

Jogo de tiro com rolagem lateral (no estilo *run and gun*) feito em Python com
pygame-ce para o Projeto Final de **Design de Software** (Insper, 2026.2).

Atravesse as fases atirando nos soldados inimigos, desvie dos tiros e dos
foguetes e chegue ao fim do mapa sem perder todas as vidas.

## Integrantes

| Integrante | Parte do projeto |
|---|---|
| Marcelo (`marcelinhorade-star`) | Jogador e tiro: `jogador.py`, `tiro.py` |
| Gabriel Gonçalves (`Gabriel2763`) | Inimigos, colisões, câmera, cenário e fases: `inimigo.py`, `colisoes.py`, `camera.py`, `cenario.py`, `efeitos.py`, `fase.py` |
| Victor Kim ("victortykim) | Loop principal, telas, HUD, som e README: `main.py`, `config.py`, `telas.py`, `hud.py`, `som.py` |

## Vídeo

LINK DO VÍDEO AQUI

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
| Setas esquerda / direita | andar |
| Seta para cima | mirar para cima |
| Seta para baixo | agachar |
| Espaço | pular |
| Z | atirar (segure para atirar sem parar) |
| ENTER | começar / jogar de novo |

## Como o código está organizado

O jogo é orientado a objetos e cada arquivo cuida de uma parte:

- `main.py`: classe `Jogo`, com o loop principal e a máquina de estados
  (`inicio` → `jogando` → `game_over` ou `vitoria` → `inicio`).
- `config.py`: constantes compartilhadas (tamanho da tela, FPS, cores, pastas).
- `telas.py`: tela de início, game over e vitória.
- `hud.py`: vida, fase e pontuação durante o jogo.
- `som.py`: música de fundo e efeitos sonoros.
- `jogador.py` / `tiro.py`: o personagem, suas animações e os tiros.
- `fase.py`, `cenario.py`, `camera.py`, `inimigo.py`, `efeitos.py`, `colisoes.py`:
  mapas das fases, fundo com paralaxe, câmera, inimigos, explosões e colisões.

## Créditos

**Imagens:** pacote "Generic RUN n' GUN", de Vaca Roxa, licença CC0.
<!-- Marcelo/Gabriel: confirmem o link do pacote e se as imagens do jogador vêm dele também. -->

**Sons e músicas:** Juhani Junkala (SubspaceAudio), licença CC0, baixados do OpenGameArt:

- [512 Sound Effects (8-bit style)](https://opengameart.org/content/512-sound-effects-8-bit-style):
  `tiro.wav` (sfx_wpn_machinegun_loop1), `dano.wav` (sfx_sounds_damage1),
  `inimigo_morre.wav` (sfx_deathscream_human1), `game_over.wav` (sfx_sounds_negative1),
  `vitoria.wav` (sfx_sounds_fanfare1).
- [5 Chiptunes (Action)](https://opengameart.org/content/5-chiptunes-action):
  `musica_menu.wav` (Title Screen) e `musica_fase.wav` (Level 1). As músicas foram
  convertidas para mono e 22 kHz para deixar o repositório menor.


