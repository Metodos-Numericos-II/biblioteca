import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Tabela:

  def __init__(self,caminho):
    self.dataframe = self.carregar_CSV(caminho)
  
  @staticmethod
  def carregar_CSV(caminho):
    '''
      Recebe o caminho e retorna o csv como um dataframe para o Pandas utilizar
    '''
    df = pd.read_csv(caminho)

    return df

  def transforma_vetor(self, df=None, colunas_categoricas = []):
    '''
      Transformar os dados categoricos (strings, por exemplo) em números aceitos pelo numpy e, se necessário, utiliza a OneHot
    '''
    if df is None:
      df = self.dataframe
    
    if len(colunas_categoricas) == 0:
      np_numerico = df.values
      header_numerico = df.columns.values
      return np_numerico, header_numerico

    df_numerico = pd.get_dummies(df, columns = colunas_categoricas) # GetDummies https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html?highlight=get_dummies#pandas.get_dummies
    header_numerico = df_numerico.columns.values # Guardar o Header dos valores numericos
    np_numerico = df_numerico.values # Transforma para formato numpy

    return np_numerico,header_numerico

  @staticmethod
  def transforma_df(np_numerico, header_numerico):
    '''
      Transformar os dados numericos para categoricos (desfazer o OneHot, nesse caso)
    '''
    ultima_col = ' ' # variavel para auxiliar a juncao do numerico em categorico
    novo_header = [] # novo header categorico
    categoria = {} # dicionario idx_coluna > categoria (para auxiliar segundo loop)
    lista_inicio_fim = [] # lista de inicios e fins (para auxiliar segundo loop)

    for idx,col_name in enumerate(header_numerico): # para cada nome no header numerico
      if '_' in col_name: # se for de categoria binaria (evidenciado pelo '_')
        split_name = col_name.split('_') # pegamos as duas partes
        if split_name[0] == ultima_col: # se estamos no mesmo nome do anterior
          lista_inicio_fim[-1][1] = idx
        else:
          novo_header.append(split_name[0])
          ultima_col = split_name[0]
          lista_inicio_fim.append([idx,idx])
        categoria[idx] = split_name[1]
      else:
        novo_header.append(col_name)

    np_new = np_numerico.astype('object')

    for coluna in lista_inicio_fim:
      for j in range(coluna[0],coluna[1]+1):
        for i in np.where(np_numerico[:,j]==1):
          np_new[i,coluna[0]] = categoria[j]

    colunas_deletadas = []
    for coluna in lista_inicio_fim:
      colunas_deletadas.extend(range(coluna[0]+1,coluna[1]+1))
      
    np_new=np.delete(np_new,colunas_deletadas,1)

    return pd.DataFrame(np_new, columns=novo_header)

  def plot_categoria_quantidade(self, coluna):
    '''
      Plota o grafico mostrando quanta cada categoria tem de quantidade
    '''

    df=self.dataframe
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])

    np_numerico, header_display = self.transforma_vetor(df[[coluna]], [coluna])

    for idx,s in enumerate(header_display):
      header_display[idx] = s.split('_')[1]

    ax.bar(header_display, np.sum(np_numerico, axis=0))
    plt.plot()

  @staticmethod
  def divide_vetor(vetor, pos, eixo = 0):
    '''
      Dividir o vetor no local especificado, podendo ser por coluna (quando parametro eixo = 1, ou por linha quando eixo = 0)
    '''
    p = [pos]
    vetor_lins, vetor_cols = np.split(vetor, p, eixo)

    return vetor_lins, vetor_cols
  
  @staticmethod
  def calcula_distancia(vetor1, vetor2):
    '''
      Calcular a distância entre vetor1 e vetor2
    '''
    # dist(vetor1,vetor2) = (y1-x1)^2 + (y2-x2)^2 + (y3-x3)^2
    # dist(vetor1,vetor2) = (vetor1[0]-vetor2[0])^2 + (vetor1[1]-vetor2[1])^2 + (vetor1[2]-vetor1[2])^2
    return np.linalg.norm(vetor1 - vetor2)

  ## Está certo? Parecer muito específico para o que temos na aplicação de sistemas de recomendação ##
  @staticmethod
  def ranquear_por_genero(generos, gxf):
    '''
      generos: recebe os generos de um filme ou generos que são a preferência do usuário
      gxf: dataframe que possui a relação gêneros por filme
    '''
    gxf_np,gxf_cols = transforma_vetor(gxf)
    gxf_np = divide_vetor(gxf_np, 1, 1)[1] # como função retorna dois valores, colocamos o [1] ao final da sua chamada para salvar o segundo valor
    gxf_cols = divide_vetor(gxf_cols, 1)[1]

    rank = []
    for i in range(len(gxf_cols)):
      dist = calcula_distancia(generos, gxf_np[:,i])
      rank.append((gxf_cols[i], dist))
    
    rank.sort(key=lambda tup:tup[1])
    return rank