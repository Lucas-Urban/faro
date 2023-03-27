from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import os

# Limpa a sessão do Keras e define as configurações da GPU
tf.keras.backend.clear_session()
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
set_session(session)

# Define as dimensões das imagens
img_altura, img_largura = 224, 224

with tf.device('/CPU:0'):
    # Carrega o modelo da rede neural treinado com o dataset Stanford Dogs
    modelo = tf.keras.models.load_model('modelo_dogs.h5')

    # Carrega o dataset Kaggle Dog Breed Identification
    data_dir = './IA/dog-breed-identification'
    test_filenames = os.listdir(os.path.join(data_dir, 'test'))
    test_images = []
    for filename in test_filenames:
        img_path = os.path.join(data_dir, 'test', filename)
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(img_altura, img_largura))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.0
        test_images.append(img)
    test_images = np.concatenate(test_images, axis=0)

    # Faz predições com o dataset Kaggle Dog Breed Identification
    predicoes = modelo.predict(test_images)

    # Avalia o modelo com o dataset Kaggle Dog Breed Identification
    resultado_teste = modelo.evaluate(test_images, batch_size=32)
    print('Acurácia no conjunto de teste:', resultado_teste[1])
