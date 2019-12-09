
from game_engine import GameEngine
from game import Game
import sys, pygame
pygame.init()

# --------------------------

jogo = Game()

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        sys.exit()
      if event.key == pygame.K_SPACE and event.mod & pygame.KMOD_LCTRL:
        jogo.novoJogo()
      # elif event.key == pygame.K_SPACE:
      #   game.moverCobra( proxDir )

      if event.key == pygame.K_d:
        jogo.proxDir = GameEngine.DIREITA
      if event.key == pygame.K_a:
        jogo.proxDir = GameEngine.ESQUERDA
      if event.key == pygame.K_w:
        jogo.proxDir = GameEngine.CIMA
      if event.key == pygame.K_s:
        jogo.proxDir = GameEngine.BAIXO

  jogo.esperarTick()
  jogo.draw()
  pass



