from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from statistics import mode
from faro_ia import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from geopy.distance import geodesic


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1123@localhost/faro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = './upload'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class EncontrarPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    local = db.Column(db.String(200))
    tutor_nome = db.Column(db.String(200))
    tutor_email = db.Column(db.String(100))
    tutor_telefone = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    fotos = db.relationship('EncontrarPetFoto', backref='encontrar_pet', lazy=True)

class EncontrarPetFoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_pet_id = db.Column(db.Integer, db.ForeignKey('encontrar_pet.id', ondelete='CASCADE'), nullable=False)
    arquivo = db.Column(db.String(50))

class EncontrarTutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(200))
    anjo_nome = db.Column(db.String(200))
    anjo_email = db.Column(db.String(100))
    anjo_telefone = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    fotos = db.relationship('EncontrarTutorFoto', backref='encontrar_tutor', lazy=True)

class EncontrarTutorFoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_tutor_id = db.Column(db.Integer, db.ForeignKey('encontrar_tutor.id', ondelete='CASCADE'), nullable=False)
    arquivo = db.Column(db.String(50))

class RacaPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raca = db.Column(db.String(50))
    encontrar_pet_id = db.Column(db.Integer, db.ForeignKey('encontrar_pet.id', ondelete='CASCADE'), nullable=False)

class RacaTutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raca = db.Column(db.String(50))
    encontrar_tutor_id = db.Column(db.Integer, db.ForeignKey('encontrar_tutor.id', ondelete='CASCADE'), nullable=False)


@app.route('/')
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
    
    # Prepara a mensagem de sucesso
    classes = []
    for foto in inputFotosPet:
        classe = classificar_imagem(foto)
        classes.append(classe)
        
    classe_mais_frequente = mode(classes)

    # Adicione 1 para obter a raça correspondente
    raca = classe_mais_frequente
    
    # Cria o objeto encontrar_pet
    encontrar_pet = EncontrarPet(nome=inputNomePet, local=inputLocalPet, tutor_nome=inputNomeTutor, tutor_email=inputEmailTutor, tutor_telefone=inputTelefoneTutor, raca= raca, latitude= latLocalPet, longitude= longLocalPet)

    # Processa as imagens e adiciona à lista de encontrar_pet_fotos do encontrar_pet
    for foto in inputFotosPet:
        arquivo = secure_filename(foto.filename)
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo)
        foto.save(caminho_arquivo)
        nova_foto = EncontrarPetFoto(arquivo=arquivo)
        encontrar_pet.fotos.append(nova_foto)

    # Salva o encontrar_pet e suas encontrar_pet_fotos no banco de dados
    db.session.add(encontrar_pet)
    db.session.commit()

    mensagem = f"Pet encontrado! Nome: {inputNomePet}, Local: {inputLocalPet}, Nome do Tutor: {inputNomeTutor}, E-mail: {inputEmailTutor}, Telefone: {inputTelefoneTutor} raça: {raca}"
    print(mensagem)  # Apenas para depuração

    return jsonify({'mensagem': mensagem}), 200

@app.route('/encontrar_tutor', methods=['POST'])
def encontrar_tutor():
    inputLocalEncontrarTutor = request.form.get('inputLocalEncontrarTutor')
    inputFotosPet = request.files.getlist('inputFotoEncontrarTutor[]')
    inputNomeAnjo = request.form.get('inputNomeAnjo')
    inputEmailAnjo = request.form.get('inputEmailAnjo')
    inputTelefoneAnjo = request.form.get('inputTelefoneAnjo')
    latLocalEncontrarTutor = request.form.get('latLocalEncontrarTutor')
    longLocalEncontrarTutor = request.form.get('longLocalEncontrarTutor')

    # Prepara a mensagem de sucesso
    classes = []
    for foto in inputFotosPet:
        classe = classificar_imagem(foto)
        classes.append(classe)
        
    classe_mais_frequente = mode(classes)

    # Adicione 1 para obter a raça correspondente
    raca = classe_mais_frequente
    
    # Cria o objeto encontrar_tutor
    encontrar_tutor = EncontrarTutor(local=inputLocalEncontrarTutor, anjo_nome=inputNomeAnjo, anjo_email=inputEmailAnjo, anjo_telefone=inputTelefoneAnjo, raca= raca, latitude= latLocalEncontrarTutor, longitude= longLocalEncontrarTutor)

    # Processa as imagens e adiciona à lista de encontrar_tutor_fotos do encontrar_tutor
    for foto in inputFotosPet:
        arquivo = secure_filename(foto.filename)
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo)
        foto.save(caminho_arquivo)
        nova_foto = EncontrarTutorFoto(arquivo=arquivo)
        encontrar_tutor.fotos.append(nova_foto)

    # Salva o encontrar_tutor e suas encontrar_tutor_fotos no banco de dados
    db.session.add(encontrar_tutor)
    db.session.commit()

    mensagem = f"Pet encontrado! Local: {inputLocalEncontrarTutor}, Nome do anjo: {inputNomeAnjo}, E-mail: {inputEmailAnjo}, Telefone: {inputTelefoneAnjo} raça: {raca}"
    print(mensagem)  # Apenas para depuração
 
    return jsonify({'mensagem': mensagem}), 200

@app.route('/encontrar_pet_tutor/<encontrar_pet_id>', methods=['GET'])
def encontrar_pet_tutor(encontrar_pet_id):
    # consulta o pet com o ID correspondente e extrai a sua localização
    encontrar_pet = EncontrarPet.query.get(encontrar_pet_id)
    
    if encontrar_pet is None:
        return jsonify({'message': 'Pet não encontrado'}), 404
    
    pet_latitude = encontrar_pet.latitude
    pet_longitude = encontrar_pet.longitude
    raca = encontrar_pet.raca

    # consulta os tutores com a mesma raça e filtra aqueles que estão a no máximo 10 quilômetros de distância do pet
    tutores = EncontrarTutor.query.filter_by(raca=raca).all()
    tutores_filtrados = []
    for tutor in tutores:
        dist_tutor = geodesic((pet_latitude, pet_longitude), (tutor.latitude, tutor.longitude)).km
        if dist_tutor <= 10:
            tutores_filtrados.append({
                'id': tutor.id,
                'local': tutor.local,
                'anjo_nome': tutor.anjo_nome,
                'anjo_email': tutor.anjo_email,
                'anjo_telefone': tutor.anjo_telefone,
                'raca': tutor.raca,
                'fotos': [foto.arquivo for foto in tutor.fotos],
                'distancia': dist_tutor
            })

    # monta o objeto de resposta em JSON, incluindo os dados do pet
    resposta = {
        'pet': {
            'id': encontrar_pet.id,
            'nome': encontrar_pet.nome,
            'local': encontrar_pet.local,
            'tutor_nome': encontrar_pet.tutor_nome,
            'tutor_email': encontrar_pet.tutor_email,
            'tutor_telefone': encontrar_pet.tutor_telefone,
            'raca': encontrar_pet.raca,
            'fotos': [foto.arquivo for foto in encontrar_pet.fotos],
            'latitude': encontrar_pet.latitude,
            'longitude': encontrar_pet.longitude
        },
        'tutores': tutores_filtrados
    }
    
    # retorna a resposta em JSON
    return jsonify(resposta),200
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')