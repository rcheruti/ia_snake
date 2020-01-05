
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

# 11: porcentagem de espaços vazios no quadro 1 (esquerda cima)
# 12: porcentagem de espaços vazios no quadro 2 (direita cima)
# 13: porcentagem de espaços vazios no quadro 3 (esquerda baixo)
# 14: porcentagem de espaços vazios no quadro 4 (direita baixo)

# Saídas:
# 0: prob esquerda
# 1: prob frente
# 2: prob direita

# --------------------------------------

def criarEntradas(game: GameEngine):
  entradas = [0] * 15
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

  # verificar areas com melhor espaço de movimento (sem considerar a cabeça da cobra)
  # quanto maior o numero, mais espaço livre existe naquela direção
  mapaArea = { '1': 0 , '2': 0 , '3': 0 , '4': 0 }
  metadeX = game.tamanhoX / 2
  metadeY = game.tamanhoY / 2
  quadroQtd = metadeX * metadeY
  for i in range( 1, len( game.corpo ) ):
    pos = game.corpo[ i ]
    if pos[ 1 ] <  metadeY and pos[ 0 ] <  metadeX : mapaArea['1'] += 1
    if pos[ 1 ] <  metadeY and pos[ 0 ] >= metadeX : mapaArea['2'] += 1
    if pos[ 1 ] >= metadeY and pos[ 0 ] <  metadeX : mapaArea['3'] += 1
    if pos[ 1 ] >= metadeY and pos[ 0 ] >= metadeX : mapaArea['4'] += 1
    pass
  entradas[ 11 ] = mapaArea['1'] / quadroQtd
  entradas[ 12 ] = mapaArea['2'] / quadroQtd
  entradas[ 13 ] = mapaArea['3'] / quadroQtd
  entradas[ 14 ] = mapaArea['4'] / quadroQtd

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

def hashEntradas(entradas: list):
  chave = ''
  for i in range(0, len(entradas)):
    chave += str( entradas[i] )
  return chave

# Bellman Equation com Q-Learning
def bellman(qAtual, probAtual, premio, desconto, qFuturo):
  # qValue = qAtual + probAtual * ( premio + desconto * qFuturo - qAtual )
  qValue = qAtual + probAtual * ( premio + qFuturo - qAtual )
  return qValue
