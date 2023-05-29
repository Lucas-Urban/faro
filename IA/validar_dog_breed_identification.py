import os
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
from keras.models import load_model
import pandas as pd

from rotulos_associados import rotulos_stanford, rotulos_kaggle, mapeamento_rotulos

# Carrega o modelo treinado
modelo_treinado = load_model('C:\\Users\\lucas\\OneDrive\\Documentos\\GitHub\\faro\\IA\\modelo_dogs.h5')

# Define o diretório do conjunto de dados
diretorio_teste = 'C:\\Users\\lucas\\OneDrive\\Documentos\\GitHub\\faro\\IA\\dog-breed-identification\\test'

# Carrega o arquivo de rótulos (breeds)
arquivo_rotulos = 'C:\\Users\\lucas\\OneDrive\\Documentos\\GitHub\\faro\\IA\\dog-breed-identification\\labels.csv'

# Carrega o arquivo de rótulos (breeds)
rotulos_df = pd.read_csv(arquivo_rotulos)
rotulos_dict = dict(zip(rotulos_df.id, rotulos_df.breed))

# Define o tamanho da imagem de entrada
img_altura, img_largura = 224, 224

# Preprocessa a imagem de entrada
def preprocess_image(image):
    image = image.resize((img_altura, img_largura))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image

# Realiza a predição para cada imagem de teste
acuracia_total = 0.0
num_total_exemplos = 0

for imagem_nome in os.listdir(diretorio_teste):
    imagem_path = os.path.join(diretorio_teste, imagem_nome)

    # Carrega a imagem
    imagem = load_img(imagem_path)

    # Pré-processa a imagem
    imagem = preprocess_image(imagem)

    # Realiza a predição utilizando o modelo treinado
    predicao = modelo_treinado.predict(imagem)
    predicao_label = np.argmax(predicao)
    classe_predita = mapeamento_rotulos[predicao_label]

    # Obtém o rótulo real da imagem
    imagem_id = os.path.splitext(imagem_nome)[0]
    rótulo_real = rotulos_dict.get(imagem_id)
    if rótulo_real is None:
        rótulo_real = rotulos_kaggle.get(imagem_id)
        if rótulo_real is None:
            try:
                rótulo_stanford_index = rotulos_stanford.index(imagem_id)
                rótulo_real = mapeamento_rotulos.get(rótulo_stanford_index)
            except ValueError:
                rótulo_real = None

    # Verifica se a predição está correta
    if rótulo_real == classe_predita:
        acuracia_total += 1.0
    num_total_exemplos += 1

    # Imprime informações sobre a imagem e a predição
    print('Imagem_id:', imagem_id)
    print('Imagem:', imagem_nome)
    print('Rótulo real:', rótulo_real)
    print('Predição:', classe_predita)
    print('---')

acuracia = acuracia_total / num_total_exemplos
print('Acurácia:', acuracia)
