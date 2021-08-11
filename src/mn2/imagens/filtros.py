from Imagem import *

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