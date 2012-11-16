import copy
import random
import math

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
      passos = 4
    passos = int(''.join(map(str,self.cromossomo[5:7])),2)
    if passos == 0:
      passos = 4
    return direcao, olhar, passos
    
  def evaluate(self, pinguim, abelha, diamantes):
    """ Fitness """
    #pinguim.x, pinguim.y 
    #abelha.x, abelha.y
    #for diamante in diamantes:
    #  pass
    #import pdb;pdb.set_trace()
    direcao, olhar, passos =  self.valor()
    fx = random.random()
    #fx = x*math.sin((10*math.pi)*x) + 1.0
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
    

class AGPinguim():
  """ """
  def __init__(self, tampop, maxgeracao, taxa_crossover, taxa_mutacao, pinguim, abelha, diamantes):
    self.abelha = abelha
    self.diamantes = diamantes
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
        individo.evaluate(self.pinguim, self.abelha, self.diamantes)
    

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
          individual.evaluate(self.pinguim, self.abelha, self.diamantes)
          next_population.append(individual)
    self.pop = next_population[:len(self.pop)]
    
  def run(self):
    while not self._goal():
      self.step()
    return self.melhor_individuo.valor()

  def _goal(self):
    return self.geracao > self.maxgeracao

  def step(self):
    self.pop.sort()
    self._nextpopulation()
    self.geracao+=1
    self.report()
  
def main():
  #      (tampop, maxgeracao, taxa_crossover, taxa_mutacao, pinguim, abelha, diamantes)
  pinguim = None
  abelha = None
  diamantes = None
  ag = AGPinguim(10, 50, 0.90, 0.01, pinguim, abelha, diamantes)
  ag.run()

if __name__ == "__main__":
  main()  
