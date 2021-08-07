import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from librosa import load
from librosa.feature import mfcc
from matplotlib.animation import FuncAnimation 

from matplotlib import rc
rc('animation', html='jshtml')

# Definições
class Sinais:
  @staticmethod
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
@staticmethod
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
@staticmethod
def normalizar(vetor):
  '''
    Parametros:
      entrada = 
        vetor: um vetor de valores
        
    Retorno: Vetor normalizado de norma 1.
    '''
  return vetor/np.linalg.norm(vetor)
@staticmethod
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
@staticmethod
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

@staticmethod
def padroniza_audio( audio_vet, tamanho ):
  '''
  Parametros:
    audio_vet: Vetor extraído do áudio,
    tamanho: Tamanho padrão que será usado.
        
  Retorno: Vetor do áudio com tamanho padronizado.
  '''
  if audio_vet.shape[0] < tamanho:
    novo_audio_data = np.zeros(tamanho) # Cria novo vetor de zeros com tamanho padrão
    novo_audio_data[:audio_vet.shape[0]] = audio_vet.astype(np.float32) # Preenche o inicio do novo vetor com o vetor de entrada
  else:
    novo_audio_data = audio_vet[:tamanho].astype(np.float32) # Corta o vetor até o temanho padrão
  
  return novo_audio_data

@staticmethod
def preprocessa_dataset_audio( por_dataset_teste=10 ):
  '''
  Antes de executar essa função, é preciso baixar o dataset de áudios de números utilizando 'git clone https://github.com/Jakobovski/free-spoken-digit-dataset.git'.

  Parametros:
    por_dataset_teste: Porcentagem dos vetores que serão usados para o dataset de teste (default = 10%).
        
  Retorno: 
    X_treino: Matriz onde cada linha é um vetor do dataset de treino,
    X_teste: Matriz onde cada linha é um vetor do dataset de teste,
    Y_treino: Vetor com a classificação de cada linha de X_treino,
    Y_teste: Vetor com a classificação de cada linha de X_teste.
  '''
  # Lista com os nomes usados nos caminhos dos arquivos
  names = ['jackson', 'nicolas', 'theo', 'yweweler', 'george', 'lucas']

  # Listas auxiliares
  audio_data_teste = []
  audio_data_treino = []
  labels_treino = []
  labels_teste = []

  # Variável para determinar o maior tamanho de vetor entre os áudios
  max_size = 0

  # Percorre por todos os arquivos de áudio
  for i in range(10):
    for name in names:
      for j in range(50):
        # Carrega o vetor do áudio
        data, sr = load("free-spoken-digit-dataset/recordings/" + str(i) + "_" + name + "_" + str(j) + ".wav", sr=None)
        
        # Separa entre a parte de treino e a parte de teste
        if j <= (por_dataset_teste * 50)/100 - 1:
          audio_data_teste.append(data)
          labels_teste.append(i)
        else:
          audio_data_treino.append(data)
          labels_treino.append(i)

        # Se encontrar tamanho de vetor maior que max_size, armazena ele
        if data.shape[0] > max_size:
          max_size = data.shape[0]

  tam_dataset_treino = len(audio_data_treino)
  tam_dataset_teste = len(audio_data_teste)

  # Inicializa os dados que serão retornados
  X_treino = np.zeros((tam_dataset_treino, max_size))
  X_teste  = np.zeros((tam_dataset_teste, max_size))
  Y_treino = np.zeros(tam_dataset_treino)
  Y_teste = np.zeros(tam_dataset_teste)

  # Preenche a matriz X e vetor Y da parte de treino
  for i in range(tam_dataset_treino):
    # Padroniza o vetor do áudio
    new_audio = padroniza_audio(audio_data_treino[i], max_size)
    X_treino[i] = new_audio
    Y_treino[i] = labels_treino[i]
    i += 1

  # Preenche a matriz X e vetor Y da parte de treino
  for i in range(tam_dataset_teste):
    # Padroniza o vetor do áudio
    new_audio = padroniza_audio(audio_data_teste[i], max_size)
    X_teste[i] = new_audio
    Y_teste[i] = labels_teste[i]
    i += 1
    
  return X_treino, X_teste, Y_treino, Y_teste

@staticmethod
def transforma_audio_mfcc( M, sr=8000, n_mfcc=13 ):
  '''
  Parametros:
    M: Matriz onde cada linha é um vetor extraído de um áudio,
    sr: Frequencia de amostragem (Sample rate) dos áudios em Hz (default = 8000),
    n_mfcc: Nº de MFCCs gerados para cada áudio (default = 13).
        
  Retorno: Matriz onde cada linha é o MFCC vetorizado da mesma linha de M.
  '''
  # Calcula o mfcc da primeira linha da matriz para saber o tamanho do vetor de resultado
  prim_mfcc = mfcc(M[0], sr=sr, n_mfcc=n_mfcc)
  tam_mfcc = prim_mfcc.shape[0] * prim_mfcc.shape[1]

  # Inicializa a matriz que será retornada
  M_mfcc = np.zeros((M.shape[0], tam_mfcc))
  # Preenche a primeira linha de M_mfcc
  M_mfcc[0] = prim_mfcc.reshape((tam_mfcc))

  # Preenche o restante de M_mfcc
  for i in range(1, M.shape[0]):
    M_mfcc[i] = mfcc(M[i], sr=sr, n_mfcc=n_mfcc).reshape((tam_mfcc))
    
  return M_mfcc

@staticmethod
def testa_modelo( modelo, X_treino, X_teste, Y_treino, Y_teste ):
  '''
  Imprime a avaliação de um modelo em relação ao dataset de treino e ao dataset de teste.

  Parametros:
    modelo: Modelo que foi treinado para a classificação; Deve ser uma classe com uma função predict(M) que recebe uma matriz,
    X_treino: Matriz onde cada linha é um vetor do dataset de treino,
    X_teste: Matriz onde cada linha é um vetor do dataset de teste,
    Y_treino: Vetor com a classificação de cada linha de X_treino,
    Y_teste: Vetor com a classificação de cada linha de X_teste.
  '''
  # Usa o modelo para predizer os datasets de treino e de teste
  Y_pred_treino = modelo.predict( X_treino )
  Y_pred_teste  = modelo.predict( X_teste )
  
  # Armazena o tamanho dos datasets de treino e de teste
  tam_treino = Y_pred_treino.shape[0]
  tam_teste  = Y_pred_teste.shape[0]

  # Inicializa os contadores de acertos
  acertos_treino = 0
  acertos_teste  = 0

  # Conta os acertos no dataset de treino
  for i in range(tam_treino):
    if Y_pred_treino[i] == Y_treino[i]:
      acertos_treino += 1

  # Conta os acertos no dataset de teste
  for i in range(tam_teste):
    if Y_pred_teste[i] == Y_teste[i]:
      acertos_teste += 1
  
  # Imprime os resultados
  print("Avaliação do modelo:")
  print("% de acertos nos dados de treino: " + str(acertos_treino/tam_treino * 100) + "%")
  print("% de acertos nos dados de teste: " + str(acertos_teste/tam_teste * 100) + "%")

@staticmethod
def classifica_audio( modelo, caminho, tam_padrao, sr=8000, n_mfcc=13 ):
  '''
  Parametros:
    modelo: Modelo que foi treinado para a classificação; Deve ser uma classe com uma função predict(M) que recebe uma matriz,
    caminho: Caminho para o arquivo de áudio que será classificado,
    tam_padrao: Tamanho para a padronização dos vetores,
    sr: Frequencia de amostragem (Sample rate) do áudio em Hz (default = 8000),
    n_mfcc: Nº de MFCCs gerados para o áudio (default = 13).
        
  Retorno: Matriz onde cada linha é o MFCC vetorizado da mesma linha de M.
  '''
  # Carrega o vetor do áudio 
  audio_data, _ = load(caminho, sr=None)
  
  # Padroniza o tamanho do audio
  audio_data_padr = padroniza_audio(audio_data, tam_padrao)
  
  # Calcula o mfcc do áudio
  audio_data_mfcc = mfcc(audio_data_padr, sr=sr, n_mfcc=n_mfcc)
  
  # Transforma o mfcc em um vetor
  audio_data_mfcc_vet = audio_data_mfcc.reshape((audio_data_mfcc.shape[0]*audio_data_mfcc.shape[1]))

  return modelo.predict([audio_data_mfcc_vet])[0]