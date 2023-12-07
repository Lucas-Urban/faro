import tensorflow as tf
import numpy as np
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import os

class_names = ["Abyssinian", "American Wirehair", "Bengal", "Birman", "Bombay", "British Shorthair", "Chausie", "Egyptian Mau", "Exotic", "LaPerm", "Lykoi", "Maine Coon", "Orange Tabby", "Persian", "Peterbald", "Ragdoll", "Russian Blue", "Scottish", "Siamese", "Sphynx", "Turkish Angora", "Tuxedo"]

# Carrega o modelo da rede neural
modelo_path = os.path.join(os.getcwd(), 'IA', 'cats', 'cat_breed_classifier.h5')
modelo = tf.keras.models.load_model(modelo_path)

# Define as dimensões das imagens
img_altura, img_largura = 224, 224

# Define o pré-processamento das imagens
def redimensiona_imagem(imagem):
    imagem = imagem.resize((img_altura, img_largura))
    imagem = np.array(imagem) / 255.0
    imagem = np.expand_dims(imagem, axis=0)
    return imagem

# Função para realizar a predição
def realizar_predicao(filename, label_resultado):
    # Adiciona a mensagem de processamento
    label_resultado.configure(text="Processando...")

    # Faz a predição da imagem e exibe o resultado na janela
    imagem = redimensiona_imagem(Image.open(filename))
    predicao = modelo.predict(imagem)[0]
    classe = class_names[np.argmax(predicao)]
    precisao = round(100 * np.max(predicao), 2)
    label_resultado.configure(text=f"Classe: {classe}\nPrecisão: {precisao}%")

# Modifica a função escolhe_imagem para chamar a função de predição
def escolhe_imagem():
    Tk().withdraw()  # esconde a janela principal do Tkinter
    filename = askopenfilename()  # abre a janela de seleção de arquivo
    imagem = Image.open(filename)  # carrega a imagem
    imagem = imagem.resize((400, 400))  # redimensiona a imagem para exibição
    imagem = ImageTk.PhotoImage(imagem)  # converte a imagem para o formato do Tkinter
    label_imagem.configure(image=imagem)  # exibe a imagem na janela
    label_imagem.image = imagem  # atualiza a referência da imagem para evitar erros de memória

    # Chama a função de predição
    realizar_predicao(filename, label_resultado)

# Define a janela do programa
janela = Tk()
janela.title("Classificador de Gatos")
janela.geometry("600x700")

# Define a imagem padrão na janela
try:
    imagem_padrao = Image.open("padrao.jpg").resize((400, 400))
except FileNotFoundError:
    # Use uma imagem padrão simples, como um quadrado branco
    imagem_padrao = Image.new("RGB", (400, 400), color="white")

# Crie o objeto PhotoImage
imagem_padrao_tk = ImageTk.PhotoImage(imagem_padrao)

# Exiba a imagem padrão na janela
label_imagem = Label(janela, image=imagem_padrao_tk)
label_imagem.image = imagem_padrao_tk  # Atualiza a referência da imagem
label_imagem.pack(pady=20)

# Define o botão para escolher a imagem
botao_escolher = Button(janela, text="Escolher Imagem", command=escolhe_imagem)
botao_escolher.pack(pady=10)

# Define o label para exibir o resultado
label_resultado = Label(janela, text="", font=("Helvetica", 16))
label_resultado.pack(pady=10)

# Inicia o loop principal do Tkinter
janela.mainloop()