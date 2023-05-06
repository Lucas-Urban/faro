from flask_mail import Mail, Message
from flask import render_template
from app import app

mail = Mail(app)

def enviar_email(encontrar_pet):
    msg = Message('Encontrar pet - Faro', sender='faroatualizacao@gmail.com', recipients=[encontrar_pet.tutor_email])
    html = render_template('email.html', encontrar_pet= encontrar_pet)
    msg.html = html

    mail.send(msg)
    
    return 'Email enviado com sucesso'
