
from game_engine import GameEngine
from game import Game
import sys, pygame
pygame.init()

import tensorflow.keras as keras
from tensorflow.keras.models import load_model

import ia_engine

# --------------------------

model = load_model('cobra.h5')
jogo = Game()
jogo.atraso = 50

def jogar():
  global model, jogo
  if jogo.game.terminado: return

  entradas = ia_engine.criarEntradas( jogo.game )
  resposta = model.predict( entradas.reshape((1, 15)) )[0]
  novaDir = ia_engine.novaDirecao( resposta, jogo.game )
  jogo.proxDir = novaDir

  jogo.esperarTick()
  jogo.draw()
  # if jogo.game.terminado:
  #   jogo.novoJogo()
  pass

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        sys.exit()
      if event.key == pygame.K_SPACE and event.mod & pygame.KMOD_LCTRL:
        keras.backend.clear_session()
        jogo.novoJogo()
      # if event.key == pygame.K_SPACE:
      #   jogar()

  jogar()
  pass



