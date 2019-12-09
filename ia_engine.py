
import numpy as np
import math
from game_engine import GameEngine

# Entradas:
# 0: fruta esta acima da cabeça?
# 1: fruta esta a direita da cabeça?
# 2: fruta esta abaixo da cabeça?
# 3: fruta esta a esquerda da cabeça?
# 4: cobra esta andando para cima?
# 5: cobra esta andando para direita?
# 6: cobra esta andando para baixo?
# 7: cobra esta andando para esquerda?
# 8: existe perigo a direita?
# 9: existe perigo a frente?
# 10: existe perigo a esquerda?

# Saídas:
# 0: prob esquerda
# 1: prob frente
# 2: prob direita

# --------------------------------------

def criarEntradas(game: GameEngine):
  entradas = [0] * 11
  cabeca = game.corpo[0]
  comida = game.comida

  entradas[0] = 1 if comida[1] < cabeca[1] else 0 # comida acima
  entradas[1] = 1 if comida[0] > cabeca[0] else 0 # comida a direita
  entradas[2] = 1 if comida[1] > cabeca[1] else 0 # comida abaixo
  entradas[3] = 1 if comida[0] < cabeca[0] else 0 # comida a esquerda

  entradas[4] = 1 if game.direcao == GameEngine.CIMA else 0
  entradas[5] = 1 if game.direcao == GameEngine.DIREITA else 0
  entradas[6] = 1 if game.direcao == GameEngine.BAIXO else 0
  entradas[7] = 1 if game.direcao == GameEngine.ESQUERDA else 0

  # verificar perigo nas bodas do jogo
  if game.direcao == GameEngine.CIMA:
    entradas[8] = 1 if cabeca[0] + 1 >= game.tamanhoX else 0
    entradas[9] = 1 if cabeca[1] - 1 < 0 else 0
    entradas[10] = 1 if cabeca[0] - 1 < 0 else 0
  elif game.direcao == GameEngine.DIREITA:
    entradas[8] = 1 if cabeca[1] + 1 >= game.tamanhoY else 0
    entradas[9] = 1 if cabeca[0] + 1 >= game.tamanhoX else 0
    entradas[10] = 1 if cabeca[1] - 1 < 0 else 0
  elif game.direcao == GameEngine.BAIXO:
    entradas[8] = 1 if cabeca[0] - 1 < 0 else 0
    entradas[9] = 1 if cabeca[1] + 1 >= game.tamanhoY else 0
    entradas[10] = 1 if cabeca[0] + 1 >= game.tamanhoX else 0
  elif game.direcao == GameEngine.ESQUERDA:
    entradas[8] = 1 if cabeca[1] - 1 < 0 else 0
    entradas[9] = 1 if cabeca[0] - 1 < 0 else 0
    entradas[10] = 1 if cabeca[1] + 1 >= game.tamanhoY else 0

  # verificar perigo com o corpo da cobra
  for i in range(1, len(game.corpo) ):
    parte = game.corpo[i]
    if game.direcao == GameEngine.CIMA:
      if parte[0] -1 == cabeca[0] and parte[1] == cabeca[1]: entradas[8] = 1
      if parte[1] +1 == cabeca[1] and parte[0] == cabeca[0]: entradas[9] = 1
      if parte[0] +1 == cabeca[0] and parte[1] == cabeca[1]: entradas[10] = 1
    elif game.direcao == GameEngine.DIREITA:
      if parte[1] -1 == cabeca[1] and parte[0] == cabeca[0]: entradas[8] = 1
      if parte[0] -1 == cabeca[0] and parte[1] == cabeca[1]: entradas[9] = 1
      if parte[1] +1 == cabeca[1] and parte[0] == cabeca[0]: entradas[10] = 1
    elif game.direcao == GameEngine.BAIXO:
      if parte[0] +1 == cabeca[0] and parte[1] == cabeca[1]: entradas[8] = 1
      if parte[1] -1 == cabeca[1] and parte[0] == cabeca[0]: entradas[9] = 1
      if parte[0] -1 == cabeca[0] and parte[1] == cabeca[1]: entradas[10] = 1
    elif game.direcao == GameEngine.ESQUERDA:
      if parte[1] +1 == cabeca[1] and parte[0] == cabeca[0]: entradas[8] = 1
      if parte[0] +1 == cabeca[0] and parte[1] == cabeca[1]: entradas[9] = 1
      if parte[1] -1 == cabeca[1] and parte[0] == cabeca[0]: entradas[10] = 1
    pass

  return np.array( entradas )

def novaDirecao(arrResposta, game: GameEngine):
  novaDir = None
  idxMax = np.argmax( arrResposta )
  if game.direcao == GameEngine.CIMA:
    if idxMax == 0: novaDir = GameEngine.ESQUERDA
    if idxMax == 1: novaDir = GameEngine.CIMA
    if idxMax == 2: novaDir = GameEngine.DIREITA
  elif game.direcao == GameEngine.DIREITA:
    if idxMax == 0: novaDir = GameEngine.CIMA
    if idxMax == 1: novaDir = GameEngine.DIREITA
    if idxMax == 2: novaDir = GameEngine.BAIXO
  elif game.direcao == GameEngine.BAIXO:
    if idxMax == 0: novaDir = GameEngine.DIREITA
    if idxMax == 1: novaDir = GameEngine.BAIXO
    if idxMax == 2: novaDir = GameEngine.ESQUERDA
  elif game.direcao == GameEngine.ESQUERDA:
    if idxMax == 0: novaDir = GameEngine.BAIXO
    if idxMax == 1: novaDir = GameEngine.ESQUERDA
    if idxMax == 2: novaDir = GameEngine.CIMA
  
  return novaDir

def distancia(ponto1, ponto2):
  return abs( math.sqrt( math.pow( ponto1[0] - ponto2[0], 2 ) + math.pow( ponto1[1] - ponto2[1], 2 ) ) )
