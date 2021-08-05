import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

from matplotlib import rc
rc('animation', html='jshtml')

# Definições
class Sinais:

  def __init__(self):
    

  def discretizar(valor_inicial, valor_final, tamanho_vetor, funcao):
  '''
    Parametros:
      entrada = 
        valor_inicial: limite inferior do espaço
        valor_final: limite superior do espaço
        tamanho_vetor: quantidades de valores nos quais o espaço será particionado
        funcao: função a ser a aplicada ao nosso espaço
    Retorno: Array com a função aplicada a cada valor do nosso espaço discretizado
    '''
  values = np.linspace(valor_inicial, valor_final, tamanho_vetor)
  vfunc = np.vectorize(funcao)

  return vfunc(values)

def morphing(vetor1, vetor2, t):
  '''
    Parametros:
      entrada = 
        vetor1: vetor 1 de elementos que definem uma função discretizada
        vetor2: vetor 2 de elementos que definem uma função discretizada
        t: tempo t do morphing
    Retorno: Array com o morphing da vetor 1 até o vetor 2 no tempo t.
    '''
  return (1 - t)*vetor1 + t*vetor2

def normalizar(vetor):
  '''
    Parametros:
      entrada = 
        vetor: um vetor de valores
        
    Retorno: Vetor normalizado de norma 1.
    '''
  return vetor/np.linalg.norm(vetor)

def animMorphing(vetor1, vetor2, xlim=(-5, 5), ylim=(-5,5), frames=100):
  '''
    Parametros:
      entrada = 
        vetor1: vetor 1 de elementos que definem uma função discretizada
        vetor2: vetor 2 de elementos que definem uma função discretizada
        xlim: tupla com os valores de mínimo e máximo de gŕafico no eixo X.
        ylim: tupla com os valores de mínimo e máximo de gŕafico no eixo Y.
        frames: quantidade de frames da animação
    Retorno: Objeto de animação do matplotlib.
    '''
  fig = plt.figure() 
   
  axis = plt.axes(xlim = xlim, 
                ylim = ylim) 
  line, = axis.plot([], [], lw = 3)

  def init(): 
    line.set_data([], [])
    return line,
   
  def animate(i):
    x = np.linspace(-5, 5, len(vetor1))
    y = morphing(vetor1, vetor2, i/frames)
    line.set_data(x, y)
      
    return line,

  anim = FuncAnimation(fig, animate, init_func = init,
                     frames = frames, interval = 20, blit = True)
  return anim

def interpolar(pontos, grauMaximo):
  '''
    Parametros:
      entrada = 
        pontos: array de tuplas com o x e o y de pontos em um plano cartesiano.
        grauMaximo: grau da função pela qual os pontos serão aproximados
        
    Retorno: Função que aproxima os pontos de entrada.
    '''
  x = [i[0] for i in pontos]
  y = [i[1] for i in pontos]
  v = np.array([np.array(x)**i for i in range(grauMaximo,-1,-1)]).T

  coef_array = np.linalg.lstsq(v, y, rcond=0.0000000001)[0]

  return lambda x: np.sum([coef_array[i]*(x**(len(coef_array)-(i+1))) for i in range(len(coef_array))])
