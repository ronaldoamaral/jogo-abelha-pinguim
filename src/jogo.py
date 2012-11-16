import os, sys, copy
import getopt
import random
# E importaremos o pygame tambem para esse exemplo
import pygame
from pygame.locals import *

images_dir = os.path.join( "..", "img" )

WIDTH, HEIGHT, TILE = 16, 16, 40
LIM_X = 16
LIM_Y = 16
DIAMANTES = []

class Abelha():  
  def __init__(self):
    self.x, self.y = 4, 4
    abelha_png = os.path.join( images_dir, 'abelha.png' )
    self.imagem = pygame.image.load(abelha_png)

    
  def movimento(self):
    direcao = random.randint(0,7)
    passo = random.randint(0,4)
    return direcao, passo
    

class Diamante():
  ativo = True
  def __init__(self):
    self.x, self.y = self.posicionar()
    diamante_png = os.path.join( images_dir, 'diamante.png' )
    self.imagem = pygame.image.load(diamante_png)
  
  def posicionar(self):
    x = random.randint(0,LIM_X)
    y = random.randint(0,LIM_Y)
    return x,y
  

class Pinguim():
  pontuacao = 0
  def __init__(self):
    self.x, self.y = (LIM_X - 4), (LIM_Y - 4)
    self.imagens = self.carregar_imagens()
    
  def carregar_imagens(self):
    imagem_list = []
    #pinguim_png1 = os.path.join( images_dir, 'pinguim01.png' )
    pinguim_png2 = os.path.join( images_dir, 'pinguim02.png' )
    pinguim_png3 = os.path.join( images_dir, 'pinguim03.png' )
    #imagem_list.append(pygame.image.load(pinguim_png1))
    imagem_list.append(pygame.image.load(pinguim_png2))
    imagem_list.append(pygame.image.load(pinguim_png3))
    return imagem_list
  
  def imagem(self):
    i = random.randint(0,1)  
    return self.imagens[i]  

    
  def movimento(self):
    direcao = random.randint(0,7)
    passo = random.randint(0,4)
    return direcao, passo
    

class Jogo():

  def __init__(self):
    self.pinguim = Pinguim()
    self.abelha = Abelha()
    self.vencedor = False
    pygame.init()
    pygame.display.set_caption("Jogo da Abelha e o Pinguim")
    self.screen = pygame.display.set_mode((640,640))
    for i in range(5):
      obj = Diamante()
      DIAMANTES.append(obj)
    
    
    
  def iniciar(self):
    clock = pygame.time.Clock()
   
    cont = 0
    while self.vencedor == False:
      clock.tick(2) # Timer entre as jogadas
      
      # Limpando a tela
      self.screen.fill((255, 255, 255))
      
      if cont % 2 == 0:
        self.movimentar(self.pinguim, self.abelha)
        for diamante in DIAMANTES:
          self.screen.blit(diamante.imagem, (diamante.x*TILE, diamante.y*TILE)) # Desenhando os diamantes         
        self.screen.blit(self.pinguim.imagem(), (self.pinguim.x*TILE, self.pinguim.y*TILE)) # Movimentando o Pinguim      
        self.screen.blit(self.abelha.imagem, (self.abelha.x*TILE, self.abelha.y*TILE)) # Movimentando a Abelha

      else: 
        self.movimentar(self.abelha, self.pinguim)
        for diamante in DIAMANTES:
          self.screen.blit(diamante.imagem, (diamante.x*TILE, diamante.y*TILE)) # Desenhando os diamantes     
        self.screen.blit(self.pinguim.imagem(), (self.pinguim.x*TILE, self.pinguim.y*TILE)) # Movimentando o Pinguim      
        self.screen.blit(self.abelha.imagem, (self.abelha.x*TILE, self.abelha.y*TILE)) # Movimentando a Abelha

        if self.pinguim.x == self.abelha.x and self.pinguim.y == self.abelha.y:
          self.vencedor = True

      print "====== Jogada " + str(cont) + "=============="     
      print "Pinguim X=" + str(self.pinguim.x) + " Y=" + str(self.pinguim.y)
      print "Abelha X=" + str(self.abelha.x) + " Y=" + str(self.abelha.y)

      cont = cont + 1
      pygame.display.flip() # Atualizacao da tela
     
      
        
  def movimentar(self, obj1, obj2):
    #import pdb;pdb.set_trace()
    direcao, passo = obj1.movimento()
    self.mover(obj1, obj2, direcao, passo)
  
  def mover(self, obj1, obj2, direcao, passo=1):
    """ 
     Direcao:
     0 = Direita
     1 = Para Baixo /Direita
     2 = Para Baixo
     3 = Para Baixo / Esquerda
     4 = Esquerda
     5 = Para Cima / Esquerda
     6 = Para Cima
     7 = Para Cima / Direita
     
     Passo = Quantidade de Casas que ira se mover. 
    
    """
    if direcao == 0:# Direita
      for i in range(passo):
        if (obj1.x + 1) in range(LIM_X):
          obj1.x = obj1.x + 1
        else:
          break
            
    elif direcao == 1: # Para Baixo / Direita
      for i in range(passo):
        if (obj1.x + 1) in range(LIM_X):
          obj1.x = obj1.x + 1
        else:
          break
      for i in range(passo):
        if (obj1.y + 1) in range(LIM_Y):
          obj1.y = obj1.y + 1
        else:
          break
        
    elif direcao == 2: # Para Baixo
      for i in range(passo):
        if (obj1.y + 1) in range(LIM_X):
          obj1.y = obj1.y + 1
        else:
          break
        
    elif direcao == 3: # Para Baixo / Esquerda
      for i in range(passo):
        if (obj1.x - 1) in range(LIM_X):
          obj1.x = obj1.x - 1
        else:
          break
      for i in range(passo):
        if (obj1.y + 1) in range(LIM_Y):
          obj1.y = obj1.y + 1
        else:
          break
      
    elif direcao == 4:# Esquerda 
      for i in range(passo):
        if (obj1.x - 1) in range(LIM_X):
          obj1.x = obj1.x - 1
        else:
          break
          
    elif direcao == 5:# Para Cima / Esquerda
      for i in range(passo):
        if (obj1.x - 1) in range(LIM_X):
          obj1.x = obj1.x - 1
        else:
          break
      for i in range(passo):
        if (obj1.y - 1) in range(LIM_Y):
          obj1.y = obj1.y - 1
        else:
          break
      
    elif direcao == 6:# Para Cima
       for i in range(passo):
        if (obj1.y - 1) in range(LIM_X):
          obj1.y = obj1.y - 1
        else:
          break
          
    elif direcao == 7:# Para Cima / Direita
      for i in range(passo):
        if (obj1.x + 1) in range(LIM_X):
          obj1.x = obj1.x + 1
        else:
          break
      for i in range(passo):
        if (obj1.y - 1) in range(LIM_Y):
          obj1.y = obj1.y - 1
        else:
          break
  
def main():
  jogo = Jogo()
  jogo.iniciar()
  

if __name__ == "__main__":
  main() 

  


