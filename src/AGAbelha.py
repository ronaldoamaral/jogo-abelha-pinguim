import copy
import random
import math

from jogo import LIM_X, LIM_Y

def mover(x, y, direcao, passo):
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
      if (x + 1) in range(LIM_X):
        x = x + 1
      else:
        break
          
  elif direcao == 1: # Para Baixo / Direita
    for i in range(passo):
      if (x + 1) in range(LIM_X):
        x = x + 1
      else:
        break
    for i in range(passo):
      if (y + 1) in range(LIM_Y):
        y = y + 1
      else:
        break
      
  elif direcao == 2: # Para Baixo
    for i in range(passo):
      if (y + 1) in range(LIM_X):
        y = y + 1
      else:
        break
      
  elif direcao == 3: # Para Baixo / Esquerda
    for i in range(passo):
      if (x - 1) in range(LIM_X):
        x = x - 1
      else:
        break
    for i in range(passo):
      if (y + 1) in range(LIM_Y):
        y = y + 1
      else:
        break
    
  elif direcao == 4:# Esquerda 
    for i in range(passo):
      if (x - 1) in range(LIM_X):
        x = x - 1
      else:
        break
        
  elif direcao == 5:# Para Cima / Esquerda
    for i in range(passo):
      if (x - 1) in range(LIM_X):
        x = x - 1
      else:
        break
    for i in range(passo):
      if (y - 1) in range(LIM_Y):
          y = y - 1
      else:
        break
     
  elif direcao == 6:# Para Cima
    for i in range(passo):
      if (y - 1) in range(LIM_X):
        y = y - 1
      else:
        break
          
  elif direcao == 7:# Para Cima / Direita
    for i in range(passo):
      if (x + 1) in range(LIM_X):
        x = x + 1
      else:
        break
    for i in range(passo):
      if (y - 1) in range(LIM_Y):
          y = y - 1
      else:
        break
  return x, y


class Individuo():
  """ """
  def __init__(self, nbits, cromossomo=None):
    self.nbits = nbits
    self.cromossomo = cromossomo or self.gerar_gens(self.nbits) 
    self.aptidao = None
    
  def gerar_gens(self, nbits):
    gens = []
    for i in range(nbits):
      gens.append(random.randint(0,1))
    return gens
    
  def valor(self):
    """ Retorna 3 valores correspondentes a [0-2] Direcao [3-4] Olhar [5-6] Passos"""
    direcao = int(''.join(map(str,self.cromossomo[:3])),2)
    olhar = int(''.join(map(str,self.cromossomo[3:5])),2)
    if olhar == 0:
      olhar = 4
    passos = int(''.join(map(str,self.cromossomo[5:7])),2)
    if passos == 0:
      passos = 4
    return direcao, olhar, passos
    
  def evaluate(self, abelha, pinguim):
    """ Fitness """
    direcao, olhar, passos =  self.valor()
    x,y = mover(abelha.x,abelha.y,direcao,passos)
    fx = (math.sqrt(math.pow((pinguim.x-x),2)+math.pow((pinguim.y-y),2)))*-1 # Multiplicado por -1 para modificar de max para mim
    #fx = random.random()
    self.aptidao = fx
    return fx
    
  def crossover(self,mate):
    return self._twopoint(mate)

  def mutacao(self,gene):
    self._pick(gene)

  def _pick(self,gene):
    self.cromossomo[gene] = int(not self.cromossomo[gene])

  def _twopoint(self,other):
    """ """
    left,right = self._pickPivots()
    def mate(p0,p1):
        cromossomo = p0.cromossomo[:]
        cromossomo[left:right] = p1.cromossomo[left:right]
        child = p0.__class__(self.nbits, cromossomo)
        return child
    return mate(self,other), mate(other,self)

  def _pickPivots(self):
    """ Escolhendo o ponto de corte para o crossover"""
    left = random.randrange(1,self.nbits-2)
    right = random.randrange(left,self.nbits-1)
    return left,right

  def __repr__(self):
    """ Sobrescrevendo a funcao de representacao do objeto"""
    return '<%s cromossomo="%s" aptidao=%s>' % \
        (self.__class__.__name__,
         ''.join(map(str,self.cromossomo)),self.aptidao)

  def __cmp__(self,other):
    """ Funcao de comparacao para ordenar a lista """
    return cmp(other.aptidao,self.aptidao)
    

class AGAbelha():
  """ """
  def __init__(self, tampop, maxgeracao, taxa_crossover, taxa_mutacao, abelha, pinguim):
    self.abelha = abelha
    self.pinguim = pinguim
    self.tampop = tampop
    self.maxgeracao = maxgeracao
    self.taxa_crossover = taxa_crossover
    self.taxa_mutacao = taxa_mutacao
    self.n_bits = 7
    self.pop = []
    self.geracao = 0
    self.gerar_populacao()
    for individo in self.pop:
        individo.evaluate(self.abelha, self.pinguim)
    

  def gerar_populacao(self):
    for i in range(self.tampop):
      self.pop.append(Individuo(self.n_bits)) 

  def melhor_individuo():
    def fget(self):
      return self.pop[0]
    return locals()
  melhor_individuo = property(**melhor_individuo())

    
  def _mutacao(self,individuo):
      for gene in xrange(individuo.nbits):
          if random.random() < self.taxa_mutacao:
              individuo.mutacao(gene)
    
  def report(self):
      print "="*70
      print "Geracao: " , self.geracao
      print "Melhor:       " , self.melhor_individuo   
    
  def _selecao(self):
      return self._roleta()
      
  def _roleta(self):
      compt = []
      total_score = sum([math.ceil(self.pop[i].aptidao) for i in xrange(len(self.pop))])
      for index in xrange(len(self.pop)):
          temp = [index] * int((math.ceil(self.pop[index].aptidao /total_score) * 100))
          compt.extend(temp)      
      return self.pop[random.choice(compt)]  
   
  def _nextpopulation(self):
    next_population = [copy.deepcopy(self.melhor_individuo)]
    while len(next_population) < len(self.pop):
      mate1 = self._selecao()
      if random.random() < self.taxa_crossover:
        mate2 = self._selecao()
        offspring = mate1.crossover(mate2)
      else:
        offspring = [copy.deepcopy(mate1)]
        for individual in offspring:
          self._mutacao(individual)
          individual.evaluate(self.abelha, self.pinguim)
          next_population.append(individual)
    self.pop = next_population[:len(self.pop)]
    
  def run(self):
    while not self._goal():
      self.step()
    return self.melhor_individuo.valor()

  def _goal(self):
    return (self.geracao > self.maxgeracao) or (self.melhor_individuo.aptidao == 0)

  def step(self):
    self.pop.sort()
    self._nextpopulation()
    self.geracao+=1
    self.report()
  
def main():
  #      (tampop, maxgeracao, taxa_crossover, taxa_mutacao, abelha, pinguim)
  abelha = None
  pinguim = None
  ag = AGPinguim(10, 50, 0.90, 0.01, abelha, pinguim)
  ag.run()

if __name__ == "__main__":
  main()  
