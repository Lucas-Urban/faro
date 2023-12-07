from operator import and_
import os
import uuid
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from geopy.distance import geodesic
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
import io
from PIL import Image
from flask_mail import Mail

#from py.faro_email import *
from py.faro_ia import *
from py.models import EncontrarPet, EncontrarPetFoto, RacaPet, EncontrarTutor, EncontrarTutorFoto, RacaTutor, NaoApresentar, Encontrado,db


register_adapter(np.float32, AsIs)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dante963@localhost/faro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['FOTO_FOLDER'] = './WEB/static/foto'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'faroatualizacao@gmail.com' # Coloque aqui seu email
app.config['MAIL_PASSWORD'] = 'zcuffffjapjpvlpl' # Coloque aqui sua senha

mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template("home.html")

@app.route('/encontrar_pet', methods=['POST'])
def encontrar_pet():
    inputNomePet = request.form.get('inputNomePet')
    inputLocalPet = request.form.get('inputLocalPet')
    inputFotosPet = request.files.getlist('inputFotoPet[]')
    inputNomeTutor = request.form.get('inputNomeTutor')
    inputEmailTutor = request.form.get('inputEmailTutor')
    inputTelefoneTutor = request.form.get('inputTelefoneTutor')
    latLocalPet = request.form.get('latLocalPet')
    longLocalPet = request.form.get('longLocalPet')
    
        
    # Cria o objeto encontrar_pet
    encontrar_pet = EncontrarPet(nome=inputNomePet, local=inputLocalPet, tutor_nome=inputNomeTutor, tutor_email=inputEmailTutor, tutor_telefone=inputTelefoneTutor, latitude= latLocalPet, longitude= longLocalPet)

    # Prepara a mensagem de sucesso
    racas = []
    for foto in inputFotosPet:
        classes = classificar_imagem(foto)
        classes_ordenadas = sorted(classes, key=lambda x: x['precisao'], reverse=True)
        for classe in classes_ordenadas[:3]:
            racas.append({'raca': classe['classe'], 'precisao': classe['precisao']})
    
    for raca in racas:
        nova_raca = RacaPet(raca=raca['raca'], precisao=raca['precisao'])
        encontrar_pet.racas.append(nova_raca)

    for foto in inputFotosPet:
        arquivo = secure_filename(foto.filename)
        
        imagem = Image.open(foto)
        # Converte a imagem para JPEG
        imagem_jpg = imagem.convert('RGB')
        # Salva a imagem em memória como bytes
        with io.BytesIO() as buffer:
            imagem_jpg.save(buffer, format='JPEG')
            foto_bytes = buffer.getvalue()
        
        nova_foto = EncontrarPetFoto(foto=foto_bytes)
        encontrar_pet.fotos.append(nova_foto)

    # Salva o encontrar_pet e suas encontrar_pet_fotos no banco de dados
    db.session.add(encontrar_pet)
    db.session.commit()

    retorno = {'mensagem': 'Busca cadastrada com sucesso!',
               'encontrar_pet_id': encontrar_pet.id}

    #enviar_email(encontrar_pet)

    return jsonify(retorno), 200

@app.route('/encontrar_tutor', methods=['POST'])
def encontrar_tutor():
    inputLocalEncontrarTutor = request.form.get('inputLocalEncontrarTutor')
    inputFotosPet = request.files.getlist('inputFotoEncontrarTutor[]')
    inputNomeAnjo = request.form.get('inputNomeAnjo')
    inputEmailAnjo = request.form.get('inputEmailAnjo')
    inputTelefoneAnjo = request.form.get('inputTelefoneAnjo')
    latLocalEncontrarTutor = request.form.get('latLocalEncontrarTutor')
    longLocalEncontrarTutor = request.form.get('longLocalEncontrarTutor')

    
    # Cria o objeto encontrar_tutor
    encontrar_tutor = EncontrarTutor(local=inputLocalEncontrarTutor, anjo_nome=inputNomeAnjo, anjo_email=inputEmailAnjo, anjo_telefone=inputTelefoneAnjo, latitude= latLocalEncontrarTutor, longitude= longLocalEncontrarTutor)

    # Prepara a mensagem de sucesso
    racas = []
    for foto in inputFotosPet:
        classes = classificar_imagem(foto)
        classes_ordenadas = sorted(classes, key=lambda x: x['precisao'], reverse=True)
        for classe in classes_ordenadas[:3]:
            racas.append({'raca': classe['classe'], 'precisao': classe['precisao']})
    
    
    for raca in racas:
        nova_raca = RacaTutor(raca=raca['raca'], precisao=raca['precisao'])
        encontrar_tutor.racas.append(nova_raca)

    # Processa as imagens e adiciona à lista de encontrar_tutor_fotos do encontrar_tutor
    for foto in inputFotosPet:
        imagem = Image.open(foto)
        # Converte a imagem para JPEG
        imagem_jpg = imagem.convert('RGB')
        # Salva a imagem em memória como bytes
        with io.BytesIO() as buffer:
            imagem_jpg.save(buffer, format='JPEG')
            foto_bytes = buffer.getvalue()
        
        nova_foto = EncontrarTutorFoto(foto=foto_bytes)
        encontrar_tutor.fotos.append(nova_foto)

    # Salva o encontrar_tutor e suas encontrar_tutor_fotos no banco de dados
    db.session.add(encontrar_tutor)
    db.session.commit()

    mensagem = f"Pet cadastrado com sucesso! Muito obrigado por colaborar!"
 
    return jsonify({'mensagem': mensagem}), 200

@app.route('/apresentar_busca/<encontrar_pet_id>', methods=['GET'])
def apresentar_busca(encontrar_pet_id):
    # consulta o pet com o ID correspondente e extrai a sua localização e raças
    encontrar_pet = EncontrarPet.query.get(encontrar_pet_id)
    
    
    if encontrar_pet is None:
        return jsonify({'message': 'Pet não encontrado'}), 404
    
    encontrado = Encontrado.query.filter(Encontrado.encontrar_pet_id == encontrar_pet_id).first()
    
    if encontrado is not None:
        return apresentar_pet_encontrado(encontrado.encontrar_pet_id, encontrado.encontrar_tutor_id)
    
    distancia_maxima = 15
    
    pet_latitude = encontrar_pet.latitude
    pet_longitude = encontrar_pet.longitude
    racas = [raca.raca for raca in encontrar_pet.racas]

    # consulta os tutores com as mesmas raças e filtra aqueles que estão a no máximo 15 quilômetros de distância do pet
    tutores = EncontrarTutor.query.filter(EncontrarTutor.racas.any(RacaTutor.raca.in_(racas))).all()
    tutores_filtrados = []
    for tutor in tutores:
        dist_tutor = round(geodesic((pet_latitude, pet_longitude), (tutor.latitude, tutor.longitude)).km,1)
        
        if not NaoApresentar.query.filter(and_(NaoApresentar.encontrar_pet_id == encontrar_pet_id, NaoApresentar.encontrar_tutor_id == tutor.id)).first() and dist_tutor <= distancia_maxima:

            fotos = []
            for foto in tutor.fotos:
                arquivo_temporario = io.BytesIO(foto.foto)
                arquivo = secure_filename(str(uuid.uuid4()) + '.jpg')
                caminho_arquivo = os.path.join(app.config['FOTO_FOLDER'], arquivo)
                with open(caminho_arquivo, 'wb') as arquivo_saida:
                    arquivo_saida.write(arquivo_temporario.getbuffer())
                fotos.append(arquivo)

            tutores_filtrados.append({
                'id': tutor.id,
                'local': tutor.local,
                'anjo_nome': tutor.anjo_nome,
                'anjo_email': tutor.anjo_email,
                'anjo_telefone': tutor.anjo_telefone,
                'data_hora': tutor.data.strftime("%d/%m/%Y %H:%M:%S"),
                'fotos': fotos,
                'distancia': dist_tutor
            })

    # monta o objeto de resposta em JSON, incluindo os dados do pet
    fotos = []
    for foto in encontrar_pet.fotos:
        arquivo_temporario = io.BytesIO(foto.foto)
        arquivo = secure_filename(str(uuid.uuid4()) + '.jpg')
        caminho_arquivo = os.path.join(app.config['FOTO_FOLDER'], arquivo)
        with open(caminho_arquivo, 'wb') as arquivo_saida:
            arquivo_saida.write(arquivo_temporario.getbuffer())
        fotos.append(arquivo)

    resposta = {
        'pet': {
            'id': encontrar_pet.id,
            'nome': encontrar_pet.nome,
            'local': encontrar_pet.local,
            'tutor_nome': encontrar_pet.tutor_nome,
            'tutor_email': encontrar_pet.tutor_email,
            'tutor_telefone': encontrar_pet.tutor_telefone,
            'fotos': fotos,
            'latitude': encontrar_pet.latitude,
            'longitude': encontrar_pet.longitude,
            'data_hora': encontrar_pet.data.strftime("%d/%m/%Y %H:%M:%S"),
            'id_pet_encontrado': 0
        },
        'tutores': tutores_filtrados
    }
    
    return render_template("busca.html", resposta=resposta)

def apresentar_pet_encontrado(encontrar_pet_id,encontrar_tutor_id):

    print(encontrar_pet_id)
    print(encontrar_tutor_id)
    encontrar_pet = EncontrarPet.query.get(encontrar_pet_id)
    if encontrar_pet is None:
        return jsonify({'message': 'Pet não encontrado'}), 404
    
    pet_latitude = encontrar_pet.latitude
    pet_longitude = encontrar_pet.longitude
    racas = [raca.raca for raca in encontrar_pet.racas]

    # consulta os tutores com as mesmas raças e filtra aqueles que estão a no máximo 10 quilômetros de distância do pet
    tutor = EncontrarTutor.query.get(encontrar_tutor_id)
    tutores_filtrados = []

    dist_tutor = round(geodesic((pet_latitude, pet_longitude), (tutor.latitude, tutor.longitude)).km,1)
    
    fotos = []
    for foto in tutor.fotos:
        arquivo_temporario = io.BytesIO(foto.foto)
        arquivo = secure_filename(str(uuid.uuid4()) + '.jpg')
        caminho_arquivo = os.path.join(app.config['FOTO_FOLDER'], arquivo)
        with open(caminho_arquivo, 'wb') as arquivo_saida:
            arquivo_saida.write(arquivo_temporario.getbuffer())
        fotos.append(arquivo)

    tutores_filtrados.append({
        'id': tutor.id,
        'local': tutor.local,
        'latitude': tutor.latitude,
        'longitude': tutor.longitude,
        'anjo_nome': tutor.anjo_nome,
        'anjo_email': tutor.anjo_email,
        'anjo_telefone': tutor.anjo_telefone,
        'data_hora': tutor.data.strftime("%d/%m/%Y %H:%M:%S"),
        'fotos': fotos,
        'distancia': dist_tutor
    })

    # monta o objeto de resposta em JSON, incluindo os dados do pet
    fotos = []
    for foto in encontrar_pet.fotos:
        arquivo_temporario = io.BytesIO(foto.foto)
        arquivo = secure_filename(str(uuid.uuid4()) + '.jpg')
        caminho_arquivo = os.path.join(app.config['FOTO_FOLDER'], arquivo)
        with open(caminho_arquivo, 'wb') as arquivo_saida:
            arquivo_saida.write(arquivo_temporario.getbuffer())
        fotos.append(arquivo)

    resposta = {
        'pet': {
            'id': encontrar_pet.id,
            'nome': encontrar_pet.nome,
            'local': encontrar_pet.local,
            'tutor_nome': encontrar_pet.tutor_nome,
            'tutor_email': encontrar_pet.tutor_email,
            'tutor_telefone': encontrar_pet.tutor_telefone,
            'fotos': fotos,
            'latitude': encontrar_pet.latitude,
            'longitude': encontrar_pet.longitude,
            'data_hora': encontrar_pet.data.strftime("%d/%m/%Y %H:%M:%S"),
            'id_pet_encontrado': encontrar_tutor_id
        },
        'tutores': tutores_filtrados
    }
    
    return render_template("encontrado.html", resposta=resposta)
    
@app.route('/nao_apresentar', methods=['POST'])
def nao_apresentar():
    encontrar_pet_id = request.get_json()['encontrar_pet_id']
    encontrar_tutor_id = request.get_json()['encontrar_tutor_id']
    
    nao_apresentar = NaoApresentar(encontrar_pet_id= encontrar_pet_id, encontrar_tutor_id= encontrar_tutor_id)
    
    db.session.add(nao_apresentar)
    db.session.commit()
    
    retorno = { 'mensagem': "Salvo com sucesso"}
    return jsonify(retorno), 200

@app.route('/encontrado', methods=['POST'])
def encontrado():
    encontrar_pet_id = request.get_json()['encontrar_pet_id']
    encontrar_tutor_id = request.get_json()['encontrar_tutor_id']
    
    encontrado = Encontrado(encontrar_pet_id= encontrar_pet_id, encontrar_tutor_id= encontrar_tutor_id)
    
    db.session.add(encontrado)
    db.session.commit()
    
    retorno = { 'mensagem': "Salvo com sucesso"}
    return jsonify(retorno), 200

@app.route('/remover_encontrado', methods=['POST'])
def remover_encontrado():
    encontrar_pet_id = request.get_json()['encontrar_pet_id']
    encontrar_tutor_id = request.get_json()['encontrar_tutor_id']
    
    encontrado = Encontrado.query.filter_by(encontrar_pet_id=encontrar_pet_id, encontrar_tutor_id=encontrar_tutor_id).first()
    
    if encontrado:
        db.session.delete(encontrado)
        db.session.commit()
        retorno = {'mensagem': 'Registro removido com sucesso'}
        return jsonify(retorno), 200
    else:
        retorno = {'mensagem': 'Registro não encontrado'}
        return jsonify(retorno), 404

@app.route('/delete_files', methods=['POST'])
def delete_files():
    files_to_delete = request.json['filesToDelete']
    for file in files_to_delete:
        file = file.replace('/static/foto/', '')
        file_path = os.path.join(app.config['FOTO_FOLDER'], file)

        if os.path.exists(file_path):
            os.remove(file_path)
            
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')