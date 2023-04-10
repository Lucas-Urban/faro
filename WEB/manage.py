from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Encontrar_pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    local = db.Column(db.String(100))
    foto = db.Column(db.String(50))
    tutor_nome = db.Column(db.String(100))
    tutor_email = db.Column(db.String(50))
    tutor_telefone = db.Column(db.String(20))
    raca = db.Column(db.String(50))