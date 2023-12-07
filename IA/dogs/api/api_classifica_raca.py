from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

# Cria a aplicação Flask
app = Flask(__name__)


# Define o pré-processamento das imagens
def redimensiona_imagem(imagem):
    imagem = tf.image.resize(imagem, (img_altura, img_largura))
    imagem /= 255.0
    return imagem

# Define a rota para receber as imagens
@app.route('/classificar', methods=['POST'])
def classificar_imagem(imagem):
    # Obtém a imagem enviada pelo cliente
    imagem = request.files['imagem'].read()
    imagem = tf.image.decode_jpeg(imagem, channels=3)
    imagem = tf.expand_dims(imagem, axis=0)
    
    # Faz o pré-processamento da imagem
    imagem = redimensiona_imagem(imagem)
    
    # Classifica a imagem com o modelo
    predicao = modelo.predict(imagem)[0]
    classe = class_names[np.argmax(predicao)]
    precisao = round(100 * np.max(predicao), 2)
    
    # Retorna o resultado em formato JSON
    return jsonify({'classe': classe})

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run()