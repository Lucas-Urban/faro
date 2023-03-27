import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

# Carrega o conjunto de dados Stanford Dogs
dataset, info = tfds.load('stanford_dogs', with_info=True, as_supervised=True)
class_names = np.array(info.features['label'].names)

# Carrega o modelo da rede neural
modelo = tf.keras.models.load_model('./modelo_dogs.h5')

# Define as dimensões das imagens
img_altura, img_largura = 224, 224

# Define o pré-processamento das imagens
def redimensiona_imagem(imagem):
    imagem = imagem.resize((img_altura, img_largura))
    imagem = np.array(imagem) / 255.0
    imagem = np.expand_dims(imagem, axis=0)
    return imagem

# Define a função para escolher a imagem
def escolhe_imagem():
    Tk().withdraw() # esconde a janela principal do Tkinter
    filename = askopenfilename() # abre a janela de seleção de arquivo
    imagem = Image.open(filename) # carrega a imagem
    imagem = imagem.resize((400, 400)) # redimensiona a imagem para exibição
    imagem = ImageTk.PhotoImage(imagem) # converte a imagem para o formato do Tkinter
    label_imagem.configure(image=imagem) # exibe a imagem na janela
    label_imagem.image = imagem # atualiza a referência da imagem para evitar erros de memória

    # Adiciona a mensagem de processamento
    label_resultado.configure(text="Processando...")
    
    # Faz a predição da imagem e exibe o resultado na janela
    imagem = redimensiona_imagem(Image.open(filename))
    predicao = modelo.predict(imagem)[0]
    classe = class_names[np.argmax(predicao)]
    precisao = round(100 * np.max(predicao), 2)
    label_resultado.configure(text=f"Classe: {classe}\nPrecisão: {precisao}%")

# Define a janela do programa
janela = Tk()
janela.title("Classificador de Cachorros")
janela.geometry("600x500")

# Define a imagem padrão na janela
imagem_padrao = Image.open("padrao.jpg").resize((400, 400))
imagem_padrao = ImageTk.PhotoImage(imagem_padrao)
label_imagem = Label(janela, image=imagem_padrao)
label_imagem.pack(pady=20)

# Define o botão para escolher a imagem
botao_escolher = Button(janela, text="Escolher Imagem", command=escolhe_imagem)
botao_escolher.pack(pady=10)

# Define o label para exibir o resultado
label_resultado = Label(janela, text="", font=("Helvetica", 16))
label_resultado.pack(pady=10)

# Inicia o loop principal do Tkinter
janela.mainloop()