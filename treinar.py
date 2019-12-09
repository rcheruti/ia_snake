
import tensorflow
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

import numpy as np
from game_engine import GameEngine
import ia_engine
from random import randint

print('TensorFlow: ' + str(tensorflow.__version__))
print('Keras: ' + str(keras.__version__))

# --------------------------------------

print('')
print('Criar modelo')

comModeloTreinado = True
if comModeloTreinado:
  model = load_model('cobra.h5')
else:
  entrada = Input(shape=(11,))
  rede = Dense(120, 'relu')(entrada)
  rede = Dropout(0.15)(rede)
  rede = Dense(120, 'relu')(rede)
  rede = Dropout(0.15)(rede)
  rede = Dense(80, 'relu')(rede)
  rede = Dropout(0.15)(rede)
  rede = Dense(3, 'softmax')(rede)
  model = Model(inputs=entrada, outputs=rede)
  model.compile( Adam(0.0005), 'mse' )

print('')
print('Iniciar treinamento')

partidas = 70
limite = 700
aleatorio = partidas * ( 20 if comModeloTreinado else 8 )
tamCobraInicial = 18
game = GameEngine()

recorde = 0
par = 0
while par < partidas:
  par += 1
  game.iniciar( tamCobraInicial )
  con = 0
  while not game.terminado:
    con += 1
    if con >= limite: break
    if (con % 25) == 0: print('Partida: %d, passo: %d, pontos: %d' % (par, con, game.pontos))

    entradas = ia_engine.criarEntradas( game )
    saidas = model.predict( entradas.reshape((1, 11)) )[0]

    if not comModeloTreinado and randint(0, aleatorio) < (partidas - par):
      resposta = to_categorical(randint(0, 2), 3)
    else:
      resposta = saidas

    novaDir = ia_engine.novaDirecao( resposta, game ) # nova direção que a IA encontrou
    pontuacao = game.pontos

    distancia1 = ia_engine.distancia( game.corpo[0], game.comida )
    game.moverCobra( novaDir )
    distancia2 = ia_engine.distancia( game.corpo[0], game.comida )

    premio = 0
    if game.pontos > pontuacao: # entao encontrou a comida
      premio = 1
      # temp = [0]*3
      # temp[ np.argmax(saidas) ] = 1
      # saidas = np.array(temp)

    elif game.terminado:
      premio = -1
      # saidas[ np.argmax(saidas) ] = 0
      
    else:
      if distancia1 <= distancia2: # moveu para longe
        premio = -0.15
      else: # moveu para perto
        premio = +0.10
      # saidas[ np.argmax(saidas) ] += premio

    # saidasFuturo = model.predict( entradas.reshape((1, 11)) )[0]

    # temp = saidas[ np.argmax(saidas) ]
    # novo = ( premio + 0.00 * np.amax(saidasFuturo) )
    saidas[ np.argmax(saidas) ] += premio

    # model.fit( entradas.reshape((1, 11)), saidas.reshape((1, 3)), epochs=1, verbose=0 )
    model.train_on_batch( entradas.reshape((1, 11)), saidas.reshape((1, 3)) )
    
  pass
  keras.backend.clear_session()
  recorde = recorde if recorde > game.pontos else game.pontos
  print('Partida: %d, passo: %d, pontos: %d, Game terminado, recorde: %d' % (par, con, game.pontos, recorde))

model.save('cobra.h5')
