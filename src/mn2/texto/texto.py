# Imports
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from pandas import DataFrame, Series
from sklearn.decomposition import TruncatedSVD
from numpy.linalg import norm as np_norm
from scipy.sparse.linalg import norm as sp_norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from nltk import twitter

# Definições

class Texto:

    def __init__(self, entrada, arquivo=True, stop_words=None):
        '''
        Parâmetros:
          entrada = 
            str: nome de um arquivo
            list: lista de strings
          arquivo = só importa se a entrada for uma lista
            True = a lista será tratada como uma lista de nomes de arquivos
            False = a lista será tratada como uma lista de documentos
           stop_words =
            'english' = ignora palavras de uma lista padrão do inglês
            list: lista de palavras para ignorar
            None = não ignora nenhuma palavra
        Retorno: Objeto Texto
        '''
        entrada = entrada if type(entrada) is list else open(entrada)
        vector = CountVectorizer(input='filename' if arquivo and type(entrada) is list else 'content',
                                 stop_words=stop_words)

        # Matriz Documentos X Termos
        # Documentos -> Linhas
        # Termos -> Colunas
        self.ocorrencias = vector.fit_transform(entrada)

        # Lista com as palavras
        self.palavras_distintas = vector.get_feature_names()

        self.palavras_ignoradas = vector.get_stop_words()

    def para_dataframe(self):
        '''
        Retorno: DataFrame do Pandas a partir da matriz de ocorrências
        '''
        return DataFrame(self.ocorrencias, columns=self.palavras_distintas)

    def para_frequencias(self):
        '''
        Retorno: Series do Pandas com a frequência de cada palavra
        '''
        return Series(self.ocorrencias.sum(axis=0).A1, index=self.palavras_distintas)

    def barplot(self, max=10):
        '''
        Parâmetros:
          max = número máximo de barras
        Retorno: Plot de barras
        '''
        return self.para_frequencias().sort_values()[-max:].plot.barh(fontsize=13)

    def wordcloud(self, min_ocorrencias=-1, **kwargs):
        '''
        Parâmetros:
          gt = Numero minimo de ocorrencias da palavra para aparecer
        Retorno: Imagem com um WordCloud do texto
        '''
        f = self.para_frequencias()
        return WordCloud(**kwargs) \
            .generate_from_frequencies(frequencies=f[f > min_ocorrencias]).to_image()


def fatora_svd(matriz_dt, n_bases):
    '''
    Parâmetros:
      matriz_dt = Matriz Documento-Termo
      n_bases = Número de bases a serem usadas na fatoração
    Retorno: Tupla com a matriz de bases e a matriz de coordenadas da fatoração
    '''

    # Instancia do SVD com n bases (n "pinceis")
    svd = TruncatedSVD(n_components=n_bases)

    # Matriz Documento X "Alguma Coisa" (Matriz dos "Pinceis")
    bases = svd.fit_transform(matriz_dt)
    coordenadas = svd.components_

    return bases, coordenadas


def plota_erro_svd(matriz_dt, log=False):
    '''
      Parâmetros:
        matriz_dt = Matriz Documento-Termo
        log = 
          True = Escala logarítmica
          False = Escala linear
      Retorno: Plot da curva de erros da compressão/fatoração SVD
      '''

    # Numero maximo de "pinceis"
    max_cols = matriz_dt.shape[0]
    max_range = range(1,max_cols+1)

    # Norma da matriz original
    norma_original = sp_norm(matriz_dt)

    diferencas = []

    for i in max_range:
        bases, coordenadas = fatora_svd(matriz_dt, i)
        matriz_reconstruida = bases @ coordenadas
        diferenca = abs(np_norm(matriz_reconstruida) - norma_original)
        diferencas.append(diferenca)

    plt.plot(max_range, diferencas, 'r')
    plt.ylabel('Diferença entre normas')
    plt.xlabel('Número de componentes')
    if log: 
      plt.yscale('log')
      plt.suptitle('Escala Logarítmica')
    else:
      plt.suptitle('Escala Linear')
    
    
def refaz_camadas_svd(bases, coordenadas):
    '''
    Parâmetros:
    bases = Matriz de bases gerada pelo SVD
    coordenadas = Matriz de coordenadas geradas pelo SVD
    Retorno: Lista com "camadas" da matriz reconstruídas a partir de cada uma das bases
    '''
    n_bases = bases.shape[1]
    camadas = []
    
    for i in range(n_bases):
        # Coluna i das bases X Linha i das coordenadas
        camada = np.outer(bases[:, i], coordenadas[i])
        camadas.append(camada)
        
    return camadas


def calcula_frequencias(matriz_dt, index):
    '''
    Parâmetros:
        matriz_dt = Matriz Documento-Termo
        index = Lista de nomes para as colunas(termos)
        
    Retorno: 
        Series do Pandas com a frequência de cada palavra
    '''
    return Series(matriz_dt.sum(axis=0), index=index)


def plota_barras(matriz_dt, index, max=10):
    '''
    Parâmetros:
        matriz_dt = Matriz Documento-Termo
        index = Lista de nomes para as colunas(termos)
        max = número máximo de barras
        
    Retorno: 
        Plot de barras
    '''
    frequencias = calcula_frequencias(matriz_dt, index)
    return frequencias.sort_values()[-max:].plot.barh(fontsize=13)


def plota_wordcloud(matriz_dt, index, min_ocorrencias=-1, **kwargs):
    '''
    Parâmetros:
        matriz_dt = Matriz Documento-Termo
        index = Lista de nomes para as colunas(termos)
        min_ocorrencias = Número mínimo de ocorrências da palavra para aparecer na nuvem
        
    Retorno: 
        Imagem com um WordCloud do texto
    '''
    frequencias = calcula_frequencias(matriz_dt, index)
    return WordCloud(**kwargs) \
        .generate_from_frequencies(frequencies=frequencias[frequencias > min_ocorrencias]).to_image()


def csv_para_lista(filepath, cabecalho):
    '''
    Parâmetros:
        filepath = Path para o arquivo csv
        cabecalho = Cabeçalho da coluna onde estão presentes os textos
        
    Retorno: 
        Lista com os textos extraídos da coluna do csv
    '''
    dataframe = pd.read_csv(filepath)
    return list(dataframe[cabecalho])


