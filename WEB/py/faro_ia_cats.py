import numpy as np
import tensorflow as tf
from PIL import Image

#Nome das raças inserido manualmente
class_names = ["Abyssinian", "American Wirehair", "Bengal", "Birman", "Bombay", "British Shorthair", "Chausie", "Egyptian Mau", "Exotic", "LaPerm", "Lykoi", "Maine Coon", "Orange Tabby", "Persian", "Peterbald", "Ragdoll", "Russian Blue", "Scottish", "Siamese", "Sphynx", "Turkish Angora", "Tuxedo"]

# Carrega o modelo treinado
modelo_path = 'C:/Users/Pichau/Documents/GitHub/faro/IA/cats/cat_breed_classifier.h5'
modelo = tf.keras.models.load_model(modelo_path)

# Define o número de classes e as dimensões das imagens
num_classes = 12
img_altura, img_largura = 224, 224

# Define o pré-processamento das imagens
def redimensiona_imagem(imagem):
    imagem = tf.image.resize(imagem, (img_altura, img_largura))
    imagem = tf.cast(imagem, tf.float32) / 255.0
    return imagem

# Define a função para classificar uma imagem
def classificar_gato(arquivo_imagem):

    # Lê a imagem a partir do objeto FileStorage
    imagem = tf.image.decode_image(arquivo_imagem.read(), channels=3)

    # Faz o pré-processamento da imagem
    imagem = redimensiona_imagem(imagem)
    
    # Classifica a imagem com o modelo
    predicao = modelo.predict(np.expand_dims(imagem, axis=0))[0]
    precisoes = np.round(100 * predicao, 2)
    classes = []
    for i in range(num_classes):
        if precisoes[i] > 0:
            classe = class_names[i]
            precisao = precisoes[i]
            objeto = {'classe': classe, 'precisao': precisao}
            classes.append(objeto)

    return classes