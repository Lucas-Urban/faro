import pandas as pd
import tensorflow_datasets as tfds

# Carregar os rótulos do conjunto de dados "Kaggle Dogs Breed Identification"
labels_df = pd.read_csv('C:\Users\Pichau\Documents\GitHub\faro\IA\dogs\dog-breed-identification\\labels.csv')
rotulos_kaggle = labels_df['breed']

# Dicionário de mapeamento entre os rótulos do Kaggle Dogs Breed Identification e Stanford Dogs
mapeamento_rotulos = {}

# Carregar os rótulos do conjunto de dados "Stanford Dogs"
rotulos_stanford = tfds.builder('stanford_dogs').info.features['label'].names

# Realizar a associação entre os rótulos
for indice, rotulo in enumerate(rotulos_stanford):
    raça_stanford = rotulo.split('-')[-1]
    for raça_kaggle in rotulos_kaggle:
        if raça_stanford.lower() in raça_kaggle.lower():
            mapeamento_rotulos[indice] = raça_kaggle
            break

# Exibir o mapeamento dos rótulos
#for key, value in mapeamento_rotulos.items():
    #print(f'Rótulo Stanford: {rotulos_stanford[key]} -> Rótulo Kaggle: {value}')
