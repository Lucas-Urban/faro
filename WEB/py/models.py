from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    racas = db.relationship('RacaPet', backref='encontrar_pet', lazy=True)
    data = db.Column(db.DateTime, default=datetime.now)
    tipo = db.Column(db.String(3))

class EncontrarPetFoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_pet_id = db.Column(db.Integer, db.ForeignKey('encontrar_pet.id', ondelete='CASCADE'), nullable=False)
    foto = db.Column(db.LargeBinary)    
    
class RacaPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_pet_id = db.Column(db.Integer, db.ForeignKey('encontrar_pet.id', ondelete='CASCADE'), nullable=False)
    raca = db.Column(db.String(50))
    precisao = db.Column(db.Float)

class EncontrarTutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(200))
    anjo_nome = db.Column(db.String(200))
    anjo_email = db.Column(db.String(100))
    anjo_telefone = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    fotos = db.relationship('EncontrarTutorFoto', backref='encontrar_tutor', lazy=True)
    racas = db.relationship('RacaTutor', backref='encontrar_tutor', lazy=True)
    data = db.Column(db.DateTime, default=datetime.now)
    tipo = db.Column(db.String(3))

class EncontrarTutorFoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_tutor_id = db.Column(db.Integer, db.ForeignKey('encontrar_tutor.id', ondelete='CASCADE'), nullable=False)
    foto = db.Column(db.LargeBinary)

class RacaTutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_tutor_id = db.Column(db.Integer, db.ForeignKey('encontrar_tutor.id', ondelete='CASCADE'), nullable=False)
    raca = db.Column(db.String(50))
    precisao = db.Column(db.Float)
    
class NaoApresentar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_pet_id = db.Column(db.Integer, db.ForeignKey('encontrar_pet.id', ondelete='CASCADE'), nullable=False)
    encontrar_tutor_id = db.Column(db.Integer, db.ForeignKey('encontrar_tutor.id', ondelete='CASCADE'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.now)
    
class Encontrado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encontrar_pet_id = db.Column(db.Integer, db.ForeignKey('encontrar_pet.id', ondelete='CASCADE'), nullable=False)
    encontrar_tutor_id = db.Column(db.Integer, db.ForeignKey('encontrar_tutor.id', ondelete='CASCADE'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.now)   