from sklearn.preprocessing import normalize

import networkx as nx
import numpy as np

import string
import re

class GrafoTexto:
  def __init__(self, lines, punctuation=True):
    '''Inicializador da classe
    Args
      lines(list): lista de frases
      punctuation(boolean): booleana que indica se as pontuações serão incluidas no grafo
    '''
    str_pattern = r'\b\w[\w-]+\b|[{}]+'.format(string.punctuation) if punctuation else r'\b\w[\w-]+\b'
    pattern = re.compile(str_pattern)
    parsed_lines = [pattern.findall(line.lower()) for line in lines]
    
    self.graph = nx.DiGraph()
    self.graph.add_node('start_point', subset=0)
    self.graph.add_node('end_point', subset=max([len(l) for l in parsed_lines])+1)
    
    for line in parsed_lines:
      if len(line) < 2: continue
      
      add_edge(self.graph, 'start_point', line[0])
      add_edge(self.graph, line[-1],'end_point')

      for i in range(len(line)-1):
        add_edge(self.graph, line[i], line[i+1])
      
      for i in range(len(line)):
        if 'subset' not in self.graph.nodes[line[i]] or self.graph.nodes[line[i]]['subset'] > i+1:
           self.graph.nodes[line[i]]['subset'] = i+1

    self.transition_matrix = normalize(nx.adjacency_matrix(self.graph), norm='l1', axis=1)
    
  def gera_caminho(self, max_size=50):
    '''Função que gera um caminho no grafo gerado, partindo do start_point até o end_point
    Args
      max_size(int): número máximo de itens no caminho
    Returns
      lista de palavras que formam uma frase
    '''
    atual = 0
    created_line = []
    while atual != 1 or len(created_line) >= max_size:
      probabilities = self.transition_matrix[atual].toarray()[0]
      name = np.random.choice(self.graph.nodes, 1, p=self.transition_matrix[atual].toarray()[0])[0]
      
      atual = list(self.graph.nodes).index(name)
      created_line.append(name)
    return created_line[:-1]

def add_edge(G, u, v):
  '''Função que adiciona uma aresta u->v no grafo G e atualiza seu peso se existir
  Args
    G(grafo): grafo em que a aresta será adicionada
    u(string): nome do nó que parte a aresta
    v(string): nome do nó que chega a aresta
  '''
  if G.has_edge(u, v): G[u][v]['weight'] += 1
  else: G.add_edge(u, v, weight=1)

def join_list(lista):
  '''Função que recebe uma lista de strings e concaterna, formando uma frase
  Args
    lista(list): lista de strings
  Returns
    frase formada pela lista
  '''
  res = lista[0].capitalize()
  for s in lista[1:]:
    res += s if s in string.punctuation else ' '+s
  return res

'''Exemplo de uso
lines = [
         'Você fez pastel semana passada?',
         'Eu comi pastel ontem.',
         'Ontem ele viajou.',
         'Eu estava dormindo.',
         'Sim, eu ganhei!'
]
tg = GrafoTexto(lines)
print(tg.gera_caminho())
'''
