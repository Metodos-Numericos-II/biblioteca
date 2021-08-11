import Imagem
import copy

# Clusterização com K-Means
from sklearn.cluster import KMeans

def quantizar(img, n_colors):
  """
  Reduz o número de cores da imagem para n_colors. Utiliza K-Means para quantização.

  Parametros:
  img (Image): A imagem para ser quantizada
  n_colors (int): O número de cores para se ter na nova imagem.
  """
  quantized_image = copy.deepcopy(img)
  kmeans = KMeans(n_colors).fit(img.dados)
  for i in range(len(img.dados)):
    quantized_image.dados[i] = kmeans.cluster_centers_[kmeans.labels_[i]]
  return quantized_image