
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
  entrada = Input(shape=(15,))
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

partidas = 70 # quantidade de partidas que serão jogadas para a cobra aprender a jogar
limite = 700 # limite de tentativas a a cobra pode usar, após isso iremos considerar que a cobra perdeu
aleatorio = partidas * ( 20 if comModeloTreinado else 8 )
tamCobraInicial = 12
game = GameEngine()
desconto = 0.8 # desconto aplicado ao valor Q de cada estado
qMapa = {} # mapeamento dos valores Q para cada estado
historico = None # para executar o processo de treinamento novamente

recorde = 0
par = 0
while par < partidas:
  par += 1
  game.iniciar( tamCobraInicial )
  con = 0
  historico = [] # reiniciar o historico de ações
  while not game.terminado:
    con += 1
    if con >= limite: break

    entradas = ia_engine.criarEntradas( game )
    saidas = model.predict( entradas.reshape((1, 15)) )[0]
    hashEntradas = ia_engine.hashEntradas( entradas )

    # if not comModeloTreinado and randint(0, aleatorio) < (partidas - par):
    #   resposta = to_categorical(randint(0, 2), 3)
    # else:
    #   resposta = saidas
    resposta = saidas
    maxIdx = np.argmax(saidas)

    novaDir = ia_engine.novaDirecao( resposta, game ) # nova direção que a IA encontrou
    pontuacao = game.pontos

    distancia1 = ia_engine.distancia( game.corpo[0], game.comida )
    game.moverCobra( novaDir )
    distancia2 = ia_engine.distancia( game.corpo[0], game.comida )

    # buscar os valores do estado futuro
    entradas_2 = ia_engine.criarEntradas( game )
    # saidas_2 = model.predict( entradas.reshape((1, 11)) )[0]
    hashEntradas_2 = ia_engine.hashEntradas( entradas_2 )

    premio = 0
    if game.pontos > pontuacao: # entao encontrou a comida
      premio = 1
    elif game.terminado:
      premio = -1
    else:
      if distancia1 <= distancia2: # moveu para longe
        premio = -0.15
      else: # moveu para perto
        premio = +0.10

    qAtual = qMapa[hashEntradas] if ( hashEntradas in qMapa ) else 0
    qFuturo = qMapa[hashEntradas_2] if ( hashEntradas_2 in qMapa ) else 0
    probAtual = saidas[ maxIdx ] # probabilidade da ação escolhida (a ação de maior prob.)

    # Bellman Equation com Q-Learning
    qValue = ia_engine.bellman( qAtual, probAtual, premio, desconto, qFuturo )
    qMapa[hashEntradas] = qValue # atualizar o mapeamento com o novo Valor Q para o estado atual

    saidas[ maxIdx ] += qValue
    tempArr = [True]*3
    tempArr[ maxIdx ] = False
    saidas[ tempArr ] -= qValue / 2

    # model.fit( entradas.reshape((1, 11)), saidas.reshape((1, 3)), epochs=1, verbose=0 )
    historico.append( [ entradas.reshape((1, 15)), saidas.reshape((1, 3)) ] )
    model.train_on_batch( entradas.reshape((1, 15)), saidas.reshape((1, 3)) )

    if (con % 25) == 0: print('Partida: %d, passo: %d, pontos: %d, qValue: %.3f' % (par, con, game.pontos, qValue))
    
  pass
  keras.backend.clear_session()
  recorde = recorde if recorde > game.pontos else game.pontos
  print('Partida: %d, passo: %d, pontos: %d, Game terminado, recorde: %d' % (par, con, game.pontos, recorde))

  for item in historico:
    model.train_on_batch( item[0], item[1] )
    pass

model.save('cobra.h5')
