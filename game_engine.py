import random

# No tabuleiro os seguintes numeros sao usados para registrar as pecas:
# 0: espaco vazio
# 1: comida
# 2: cabeca da cobra
# 3: corpo da cobra

# A variavel "direcao" usa os seguintes numeros para indicar para onde a cobra esta se movendo:
# 1: cima
# 2: direita
# 3: baixa
# 4: esquerda

class GameEngine:

  COMIDA = 1
  CABECA = 2
  CORPO = 3

  CIMA = 1
  DIREITA = 2
  BAIXO = 3
  ESQUERDA = 4

  def __init__(self):
    pass

  def criarComida(self):
    posicaoX = random.randint( 1, self.tamanhoX ) -1
    posicaoY = random.randint( 1, self.tamanhoY ) -1
    for pos in self.corpo:
      if pos[0] == posicaoX and pos[1] == posicaoY:
        return self.criarComida() # encontrar nova posição
    return [ posicaoX , posicaoY ]

  def iniciar(self, tamanhoCobra = 3):
    if tamanhoCobra < 3: tamanhoCobra = 3
    self.terminado = False # indica se o jogo acabou
    self.pontos = 0
    self.tamanhoX = 20
    self.tamanhoY = 20
    self.comida = 0
    self.cabeca = 0 # posicao da cabeca da cobra
    self.corpo = [] # posicao das partes da cobra, o indice 0 é a cabeca
    self.direcao = GameEngine.BAIXO # direcao que a cobra esta se movendo

    self.comida = self.criarComida()

    inicial = [ 2 , tamanhoCobra ]
    self.corpo.append( [ inicial[0] , inicial[1] ] )
    for i in range(1, tamanhoCobra):
      self.corpo.append( [ inicial[0] , inicial[1] - i ] )
    pass

  def moverCobra(self, direcao):
    # se o jogo já acabou não iremos mover cobra
    if self.terminado : return 0

    # corrigir direcao caso seja uma direcao cotraria ao movimento atual da cobra
    if( self.direcao == GameEngine.BAIXO and direcao == GameEngine.CIMA ): direcao = self.direcao
    elif( self.direcao == GameEngine.CIMA and direcao == GameEngine.BAIXO ): direcao = self.direcao
    elif( self.direcao == GameEngine.DIREITA and direcao == GameEngine.ESQUERDA ): direcao = self.direcao
    elif( self.direcao == GameEngine.ESQUERDA and direcao == GameEngine.DIREITA ): direcao = self.direcao
    self.direcao = direcao

    # encontrar nova posição da cobra
    cabeca = self.corpo[0]
    rabo = self.corpo[ len(self.corpo)-1 ]
    nova = [ 0 , 0 ]
    if( direcao == GameEngine.BAIXO ): nova = [ cabeca[0] , cabeca[1] + 1 ]
    elif( direcao == GameEngine.CIMA ): nova = [ cabeca[0] , cabeca[1] - 1 ]
    elif( direcao == GameEngine.ESQUERDA ): nova = [ cabeca[0] - 1 , cabeca[1] ]
    elif( direcao == GameEngine.DIREITA ): nova = [ cabeca[0] + 1 , cabeca[1] ]
    
    # reposicionar partes da cobra
    for i in range( len(self.corpo)-2, -1, -1 ):
      self.corpo[i+1] = self.corpo[i]
    self.corpo[0] = nova

    # verificar se encontrou a comida
    if nova[0] == self.comida[0] and nova[1] == self.comida[1]:
      self.pontos += 1
      self.comida = self.criarComida()
      self.corpo.append( rabo )

    # verificar se a cobra atingiu uma parede e perdeu o jogo
    if( nova[0] < 0 or nova[0] > self.tamanhoX-1 or nova[1] < 0 or nova[1] > self.tamanhoY-1 ): self.terminado = True
    # verificar se a cobra atingiu o proprio corpo, sem verificar a cabeça
    for i in range(1, len(self.corpo) ):
      pos = self.corpo[i]
      if( nova[0] == pos[0] and nova[1] == pos[1] ):
        self.terminado = True
        break

    pass

  pass
