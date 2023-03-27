import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np

# Carrega o conjunto de dados Stanford Dogs
dataset, info = tfds.load('stanford_dogs', with_info=True, as_supervised=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

# Define o número de classes e as dimensões das imagens
num_classes = info.features['label'].num_classes
img_altura, img_largura = 224, 224

# Define o pré-processamento das imagens
def redimensiona_imagem(imagem, label):
    imagem = tf.cast(imagem, tf.float32)
    imagem = tf.image.resize(imagem, (img_altura, img_largura))
    imagem /= 255.0
    return imagem, label

# Aplica o pré-processamento nas imagens de treinamento e teste
train_dataset = train_dataset.map(redimensiona_imagem)
test_dataset = test_dataset.map(redimensiona_imagem)

# Define o modelo da rede neural
modelo = tf.keras.Sequential([
    tf.keras.applications.MobileNetV2(input_shape=(img_altura, img_largura, 3), include_top=False),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Congela as camadas convolucionais da MobileNetV2
modelo.layers[0].trainable = False

# Compila o modelo da rede neural
modelo.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Define o nome do arquivo de log
log_filename = 'log_treinamento.txt'

# Cria um objeto file para o arquivo de log
log_file = open(log_filename, 'w')

# Cria um objeto CSVLogger para gravar o log durante o treinamento
csv_logger = tf.keras.callbacks.CSVLogger(log_filename, separator='\t')

# Treina o modelo da rede neural
batch_size = 32
epocas = 10
historico = modelo.fit(train_dataset.batch(batch_size),
                       epochs=epocas,
                       validation_data=test_dataset.batch(batch_size),
                       callbacks=[csv_logger])

# Fecha o arquivo de log
log_file.close()

# Avalia o modelo da rede neural
resultado_teste = modelo.evaluate(test_dataset.batch(batch_size))
print('Acurácia no conjunto de teste:', resultado_teste[1])

# Plota os gráficos de acurácia e perda
plt.plot(historico.history['accuracy'], label='Acurácia no conjunto de treinamento')
plt.plot(historico.history['val_accuracy'], label='Acurácia no conjunto de validação')
plt.plot(historico.history['loss'], label='Perda no conjunto de treinamento')
plt.plot(historico.history['val_loss'], label='Perda no conjunto de validação')
plt.legend()
plt.show()

# Salva o modelo
modelo.save('modelo_dogs.h5')