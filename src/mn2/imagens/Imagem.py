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


def salvar(img, caminho):
  """
  Salva a  imagem como arquivo no caminho especificado.
  img: Imagem de entrada
  caminho: Local de destino, incluindo nome do arquivo e extensão
  """
  converter_PIL(img).save(caminho)
