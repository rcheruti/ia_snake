
from game_engine import GameEngine
import ia_engine
import sys, pygame
pygame.font.init()
import PIL
import random

# -------------------------------
# carregar imagens
frutas = [
  pygame.image.load('maca.png') ,
  pygame.image.load('laranja.png')
]
for i in range( 0, len(frutas) ):
  frutas[i] = pygame.transform.scale( frutas[i], (20,20) )

# -------------------------------

tamanhoPeca = 20 # tamanho de cada peca no jogo (x,y)px
painelPontuacaoH = 70

preto = 0, 0, 0
branco = 255, 255, 255
marrom = 173, 124, 81
verde1 = 66, 173, 78
verde2 = 44, 115, 52
verm = 255, 108, 99

escrever = pygame.font.Font('Roboto-Light.ttf', 20)

# -------------------------------

class Game:
  textoX = escrever.render('X', True, (200,0,0))

  def __init__(self):
    global escrever
    self.screen = None
    self.atraso = 350 # quanto tempo entre os movimentos
    self.game = GameEngine()
    self.novoJogo()
    pass

  def novoJogo(self, tamanhoCobra = 3):
    self.game.iniciar( tamanhoCobra )
    self.width, self.height = self.game.tamanhoX * tamanhoPeca + tamanhoPeca * 2, self.game.tamanhoY * tamanhoPeca + tamanhoPeca * 2
    self.size = self.width, self.height + painelPontuacaoH
    self.proxDir = GameEngine.BAIXO
    self.clock = pygame.time.Clock()
    self.clock.tick()
    self.tempo = 0
    self.frutaIdx = random.randint( 0, len(frutas)-1 )
    if self.screen is None:
      self.screen = pygame.display.set_mode(self.size)
    pass

  def esperarTick(self):
    # permitir o movimento da cobra
    self.clock.tick()
    self.tempo += self.clock.get_time()
    if self.tempo >= self.atraso:
      self.tempo = 0
      self.game.moverCobra( self.proxDir )
      return True
    return False

  def draw(self):
    # pintar espacos da tela
    self.screen.fill(branco)
    for i in range(0, self.game.tamanhoY + 2):
      self.screen.fill( marrom, pygame.Rect( 0, i * tamanhoPeca, tamanhoPeca, tamanhoPeca ) )
      self.screen.fill( marrom, pygame.Rect( self.width -tamanhoPeca, i * tamanhoPeca, tamanhoPeca, tamanhoPeca ) )
      pass
    for i in range(0, self.game.tamanhoX + 2):
      self.screen.fill( marrom, pygame.Rect( i * tamanhoPeca, 0, tamanhoPeca, tamanhoPeca ) )
      self.screen.fill( marrom, pygame.Rect( i * tamanhoPeca, self.height -tamanhoPeca, tamanhoPeca, tamanhoPeca ) )
      pass
    
    # pintar fruta
    # self.screen.fill( verm, pygame.Rect( (self.game.comida[0]+1) * tamanhoPeca, (self.game.comida[1]+1) * tamanhoPeca, tamanhoPeca, tamanhoPeca ) )
    self.screen.blit( frutas[self.frutaIdx], ((self.game.comida[0]+1) * tamanhoPeca, (self.game.comida[1]+1) * tamanhoPeca) )
    
    # pintar corpo
    for i in range(1, len(self.game.corpo)):
      corpo = self.game.corpo[i]
      self.screen.fill( verde2, pygame.Rect( (corpo[0]+1) * tamanhoPeca, (corpo[1]+1) * tamanhoPeca, tamanhoPeca, tamanhoPeca ) )
      pass
    cabeca = self.game.corpo[0]
    self.screen.fill( verde1, pygame.Rect( (cabeca[0]+1) * tamanhoPeca, (cabeca[1]+1) * tamanhoPeca, tamanhoPeca, tamanhoPeca ) )
    # verificar e pintar 'X' na cabeça da cobra caso o jogo tenha terminado
    if self.game.terminado:
      self.screen.blit(Game.textoX, ( (cabeca[0]+1) * tamanhoPeca +4, (cabeca[1]+1) * tamanhoPeca -2 ))
      pass

    # escrever pontuação
    textoPontuacao = escrever.render('Pontuação: %d' % (self.game.pontos), True, (0,0,0))
    self.screen.blit(textoPontuacao, (20, self.height + 20))
    
    # escrever entradas do treinamento para o estado atual
    entradas = ia_engine.criarEntradas( self.game )
    # direção da fruta
    txt = '%d%d%d%d' % ( entradas[0], entradas[1], entradas[2], entradas[3] )
    self.screen.blit( escrever.render('^ > . <',  True, (160,160,160)), (200, self.height ))
    self.screen.blit( escrever.render(txt, True, (200,40,40)), (200, self.height + 20))
    self.screen.blit( escrever.render('fruta',  True, (200,200,200)), (200, self.height + 40 ))
    # direção da cobra
    txt = '%d%d%d%d' % ( entradas[4], entradas[5], entradas[6], entradas[7] )
    self.screen.blit( escrever.render('^ > . <',  True, (160,160,160)), (280, self.height ))
    self.screen.blit( escrever.render(txt, True, (20,140,20)), (280, self.height + 20))
    self.screen.blit( escrever.render('cobra',  True, (200,200,200)), (280, self.height + 40 ))
    # perigo nas direções de decisão
    txt = '%d%d%d' % ( entradas[8], entradas[9], entradas[10] )
    self.screen.blit( escrever.render('D F E',  True, (160,160,160)), (360, self.height ))
    self.screen.blit( escrever.render(txt, True, (200,40,40)), (360, self.height + 20))
    self.screen.blit( escrever.render('perigo',  True, (200,200,200)), (360, self.height + 40 ))
    
    pygame.display.flip()
    pass
