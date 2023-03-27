from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

# Cria a aplicação Flask
app = Flask(__name__)

# Carrega o modelo treinado
modelo = tf.keras.models.load_model('modelo.h5')

# Define o número de classes e as dimensões das imagens
num_classes = 120
img_altura, img_largura = 224, 224

# Define o pré-processamento das imagens
def redimensiona_imagem(imagem):
    imagem = tf.image.resize(imagem, (img_altura, img_largura))
    imagem /= 255.0
    return imagem

# Define a rota para receber as imagens
@app.route('/classificar', methods=['POST'])
def classificar_imagem():
    # Obtém a imagem enviada pelo cliente
    imagem = request.files['imagem'].read()
    imagem = tf.image.decode_jpeg(imagem, channels=3)
    imagem = tf.expand_dims(imagem, axis=0)
    
    # Faz o pré-processamento da imagem
    imagem = redimensiona_imagem(imagem)
    
    # Classifica a imagem com o modelo
    resultado = modelo.predict(imagem)
    classe = np.argmax(resultado)
    
    # Retorna o resultado em formato JSON
    return jsonify({'classe': classe})

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run()