import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds


# Carrega o conjunto de dados Stanford Dogs
dataset, info = tfds.load('stanford_dogs', with_info=True, as_supervised=True)
class_names = np.array(info.features['label'].names)

# Carrega o modelo treinado
modelo_path = 'WEB/modelo_dogs.h5'
modelo = tf.keras.models.load_model(modelo_path)

# Define o número de classes e as dimensões das imagens
num_classes = 120
img_altura, img_largura = 224, 224


# Define o pré-processamento das imagens
def redimensiona_imagem(imagem):
    imagem = imagem.resize((img_altura, img_largura))
    imagem = np.array(imagem) / 255.0
    imagem = np.expand_dims(imagem, axis=0)
    return imagem


# Define o pré-processamento das imagens
def redimensiona_imagem(imagem):
    imagem = tf.image.resize(imagem, (img_altura, img_largura))
    imagem /= 255.0
    return imagem

# Define a função para classificar uma imagem
def classificar_imagem(imagem):
    # Obtém a imagem enviada pelo cliente
    imagem = imagem.read()
    imagem = tf.image.decode_jpeg(imagem, channels=3)
    imagem = tf.expand_dims(imagem, axis=0)
    
    # Faz o pré-processamento da imagem
    imagem = redimensiona_imagem(imagem)
    
    # Classifica a imagem com o modelo
    predicao = modelo.predict(imagem)[0]
    classe = class_names[np.argmax(predicao)]
    precisao = round(100 * np.max(predicao), 2)
    
    return classe