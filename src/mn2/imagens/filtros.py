# -*- coding: utf-8 -*-

# PIL (pillow), biblioteca de imagens
from PIL import Image

# Biblioteca contendo a função de convolução
from scipy import ndimage

# Imprimir coisas no collab
from IPython.display import display, HTML
from IPython.display import Image as display_image

# Obter imagens com link
import requests

# Plots
import matplotlib.pyplot as plt

# Cálculos com arrays e matrizes
import numpy as np

# Usado para copiar instancias de objetos
import copy

class Imagem():
  def __init__(self, dados, largura, altura, formato, modo):
    self.dados = dados
    self.largura = largura
    self.altura = altura
    self.formato = formato
    self.modo = modo
 
def abrir(arquivo):
  """
  Dado o caminho para o arquivo de imagem, retOrna uma instancia de Imagem.
  """
  img = Image.open(arquivo)
  largura, altura = img.width, img.height
  # Os dados guardados serão floats entre 0 e 1 armazenados em um array unidimensional
  dados = np.array(img.getdata())/255
  formato = img.format
  modo = img.mode
  imagem = Imagem(dados, largura, altura, formato, modo)
  return imagem
 
def abrir_url(img_url):
  return abrir(requests.get(img_url, stream=True).raw)
 
def converter_PIL(imagem):
  """
  Dada uma instância de Imagem, retorna uma instancia de PIL.Image
  """
  # Convertemos o dado para o formato do PIL (valores inteiros entre 0 e 255, convertidos para uint8)
  dados = np.clip(imagem.dados * 255, 0, 255).astype(np.uint8)
  # Mudamos a forma de um vetor unidimensional para uma matriz
  if imagem.modo == "L":
    dados = dados.reshape(imagem.altura, imagem.largura)
  else:
    dados = dados.reshape(imagem.altura, imagem.largura, imagem.dados.shape[-1])
  imagem_pil = Image.fromarray(dados)
  return imagem_pil
 
def imprimir(*args):
  """
  Dadas n instâncias de imagens, exibe-as no notebook
  """
  imagens = []
 
  for imagem in args:
    imagem_imprimivel = converter_PIL(imagem)
    imagens.append(imagem_imprimivel)
  # Imprimimos utilizando pyplot para imprimir horizontalmente
  imagens_len = len(imagens)
  fig = plt.figure()
  for i in range(imagens_len):
    fig.add_subplot(1, imagens_len, i+1)
    imagem = imagens[i]
    plt.imshow(imagem,cmap='gray', vmin=0, vmax=255)
    plt.axis("off")
    plt.show()


class ErroValidacaoDeCor(Exception):
    pass

def validar_cor(modo, cor):
  comprimentos = {"RGB": 3, "RGBA": 4, "L": 1, "CMYK": 4}

  if any(not isinstance(x,(int, float)) for x in cor):
        raise ErroValidacaoDeCor("Cor inválida:" + cor)
  
  if len(cor) != comprimentos[modo]:
    raise ErroValidacaoDeCor(f"Cor incompatível com o modo {modo}: {args}")
    
def converter(img, modo, *cor_transparente):
  """
  Converte a imagem para o modo escolhido.

  Parametros:
  img (Image): A imagem para ser convertida
  modo (str): O modo da imagem ("L", "RGB", "RGBA", "CMY", "HSL")
  cor_transparente: Cor definida como transparente no caso de conversão RGBA -> RGB
  
  Retorna:
  Image: A imagem convertida
  """

  if img.modo == "RGB" and modo == "L":
    f = lambda c: sum(c)/3
  elif img.modo == "L" and modo == "RGB":
    f = lambda c: np.array([c] * 3)
  elif img.modo == "L" and modo == "RGBA":
    f = lambda c: np.append(np.array([c] * 3), 1)
  elif img.modo != "RGB" and modo == "RGBA":
    f = lambda c: [sum(c)/3, 1]
  elif img.modo == "RGBA" and modo == "L":
    f = lambda c: sum(c[:3]/3) * c[3]
  elif img.modo == "RGBA" and modo == "RGB":
    validar_cor("RGB", cor_transparente) 
    transparente = np.array(cor_transparente)
    f = lambda c: c[:3] * c[3] + transparente * (1 - c[3]) 
    
  novos_dados = np.array([f(x) for x in img.dados])
  nova_img = Imagem(novos_dados, img.largura, img.altura, img.formato, modo)  
  ## TODO: Outras conversões
  return nova_img


def filtrar_canal(img, canal, colorido=False):
  """
  Retorna uma imagem que possui apenas o canal escolhido.

  Parametros:
  img (Image): A imagem para filtrar o canal
  canal (char): O caracter correspondente do modo da imagem ("R", para "RGB")
  colorido (bool): Se verdadeiro, retorna uma imagem no modo "RGB", se falso, retorna no modo "L"

  Retorna:
  Image: A imagem apenas com o canal escolhido
  """
  nova_img = copy.deepcopy(img)
  funcoes_filtro_colorido = {
    "R": lambda c: [c[0], 0, 0],
    "G": lambda c: [0, c[1], 0],
    "B": lambda c: [0, 0, c[2]]
  }
  funcoes_filtro_cinza = {
    "R": lambda c: c[0],
    "G": lambda c: c[1],
    "B": lambda c: c[2]
  }
  if colorido:
    nova_img.dados = np.array([funcoes_filtro_colorido[canal](c) for c in img.dados ])
  else:
    nova_img.dados = np.array([funcoes_filtro_cinza[canal](c) for c in img.dados ])
    nova_img.modo = "L"
    
  return nova_img


def adicionar(img_A, B):
  """
  Adiciona img_A por B. B pode ser outra imagem, uma lista de 3 elementos ou um número.
  """
  if isinstance(B, int) or isinstance(B, float):
    B = np.array([B, B, B])
  if isinstance(B, np.ndarray) or isinstance(B, list):
    img_B = copy.deepcopy(img_A)
    img_B.dados = np.full(img_A.dados.shape, B)
  else:
    img_B = B

  nova_img = copy.deepcopy(img_A)
  nova_img.dados = img_A.dados + img_B.dados
  return nova_img

Imagem.__add__ = adicionar

def subtrair(img_A, B):
  """
  Subtrai img_A por B. B pode ser outra imagem, uma lista de 3 elementos ou um número.
  """
  if isinstance(B, int) or isinstance(B, float):
    B = np.array([B, B, B])
  if isinstance(B, np.ndarray) or isinstance(B, list):
    img_B = copy.deepcopy(img_A)
    img_B.dados = np.full(img_A.dados.shape, B)
  else:
    img_B = B

  nova_img = copy.deepcopy(img_A)
  nova_img.dados = img_A.dados - img_B.dados
  return nova_img

Imagem.__sub__ = subtrair

def multiplicar(img_A, B):
  """
  Multiplica img_A por B. B pode ser outra imagem, uma lista de 3 elementos ou um número.
  """
  if isinstance(B, int) or isinstance(B, float):
    B = np.array([B, B, B])
  if isinstance(B, np.ndarray) or isinstance(B, list):
    img_B = copy.deepcopy(img_A)
    img_B.dados = np.full(img_A.dados.shape, B)
  else:
    img_B = B

  nova_img = copy.deepcopy(img_A)
  nova_img.dados = img_A.dados * img_B.dados
  return nova_img

Imagem.__mul__ = multiplicar

def dividir(img_A, B):
  """
  Divide img_A por B. B pode ser outra imagem, uma lista de 3 elementos ou um número.
  """
  if isinstance(B, int) or isinstance(B, float):
    B = np.array([B, B, B])
  if isinstance(B, np.ndarray) or isinstance(B, list):
    img_B = copy.deepcopy(img_A)
    img_B.dados = np.full(img_A.dados.shape, B)
  else:
    img_B = B

  nova_img = copy.deepcopy(img_A)
  nova_img.dados = img_A.dados / img_B.dados
  return nova_img

Imagem.__truediv__ = dividir


def blend(img_A, img_B, n_frames):
  range_A = np.linspace(start = 1., stop = 0., num = n_frames)
  range_B = 1. - range_A

  blend_imgs = []
  for i in range(len(range_A)):
    blend_imgs = np.append(blend_imgs, img_A * range_A[i] + img_B * range_B[i])

  return blend_imgs


def salvar_gif(nome, imagens, duracao, loop=0):
  imgs_pil = []
  for img in imagens:
    imgs_pil.append(converter_PIL(img))
  imgs_pil[0].save(nome, format="GIF", save_all=True, append_images=imgs_pil[1:], duration=duracao, loop=loop)


def convoluir(img, filtro):
  """
  Convolui um kernel com uma Imagem L
  img: Imagem
  filtro: kernel (ndarray). Não reverte-lo antes de passar para a função
  retorno: Imagem resultado da convolução
  """
  nova_img = Imagem(None, img.largura, img.altura, img.formato, img.modo)
  if img.modo != "L":
    raise Exception('O modo da imagem é incompatível com esta função')
  convolucao = ndimage.convolve(
    img.dados.reshape(img.altura, img.largura),
    filtro[::-1, ::-1],
    mode="constant",
  )
  nova_img.dados = convolucao.reshape(img.largura * img.altura)
  return nova_img


def reunir_canais(img_r, img_g, img_b, img_a=None):
    """
    Cria imagem colorida RGB/RGBA a partir de três imagems em modo L.
    img_r: Imagem L para o canal vermelho
    img_g: Imagem L para o canal verde
    img_b: Imagem L para o canal azul
    img_a: Imagem L para o canal alpha
    retorno: Imagem
    """
    altura, largura = img_r.altura, img_g.largura
    novos_dados = np.zeros([altura * largura, 4 if img_a else 3] )
    for i in range(novos_dados.shape[0]):
      novos_dados[i][0] = img_r.dados[i]
      novos_dados[i][1] = img_g.dados[i]
      novos_dados[i][2] = img_b.dados[i]
    if img_a:
        novos_dados[i][3] = img_a[i]
    return Imagem(novos_dados, largura, altura, img_r.formato, "RGBA" if img_a else "RGB" )
    
        
def detectar_bordas(img, branco=None):
  """
  Retorna nova Imagem com aplicação de filtro de detecção de bordas
  img: Imagem de entrada
  branco: (float) se especificado, todo cinza maior ou igual a esse valor vira 1
  """
  vertical_sobel = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
  ], dtype="float64") 

  horizontal_sobel = np.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1]
  ], dtype="float64") 

  canais = [
    filtrar_canal(img, "R"), filtrar_canal(img, "G"), filtrar_canal(img, "B")  
  ]
    
  bordas_verticais = [convoluir(img, vertical_sobel) for img in canais]
  bordas_horizontais = [convoluir(img, horizontal_sobel)for img in canais]
   
  canais = [ x[0] * x[0] + x[1] * x[1] for x in zip(bordas_verticais, bordas_horizontais) ]
  dados = sum([img.dados for img in canais]) / 3

  if branco:
    dados = dados >= branco

  return Imagem(dados, img.largura, img.altura, img.formato, "L")


def blur_gaussiano(img, n=1):
  """
  Aplica blur gaussiano na imagem e retorna a nova imagem
  img: Imagem de entrada
  n: (int) número de vezes que o filtro será aplicado
  retrno: Imagem com o filtro aplicado
  """
  kernel = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
      
  ], dtype="float64") / 16
  if img.modo == "L":
    return convoluir(img, kernel)
  canais = [
    filtrar_canal(img, "R"), filtrar_canal(img, "G"), filtrar_canal(img, "B")  
  ]

  for i in range(0, n):
    canais = [convoluir(i, kernel) for i in canais]

  return reunir_canais(*canais)


def nitidez(img):
  """
  Aplica um filtro de nitidez (unsharpen mask) na imagem e retorna a nova imagem.
  img: Imagem de entrada
  retorno: Imagem com o filtro aplicado 
  """
  kernel = np.array([
      [0, -1, 0],
      [-1, 5, -1],
      [0, -1, 0]
  ])
  if img.modo == "L":
    return convoluir(img, kernel)
  canais = [
    filtrar_canal(img, "R"), filtrar_canal(img, "G"), filtrar_canal(img, "B")  
  ]
  canais = [convoluir(i, kernel) for i in canais]
  return reunir_canais(*canais)

def salvar(img, caminho):
  """
  Salva a  imagem como arquivo no caminho especificado.
  img: Imagem de entrada
  caminho: Local de destino, incluindo nome do arquivo e extensão
  """
  converter_PIL(img).save(caminho)
