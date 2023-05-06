from flask_mail import Mail, Message
from app import app

mail = Mail(app)

def enviar_email(encontrar_pet_id, email_tutor):
    msg = Message('Encontrar pet - Faro', sender='faroatualizacao@gmail.com', recipients=[email_tutor])
    msg.body = f'Olá! O seu pedido de busca com id {encontrar_pet_id} foi cadastrado com sucesso em nosso sistema. Em breve entraremos em contato caso tenhamos novidades. Obrigado!'

    mail.send(msg)