from flask import Flask, request

app = Flask(__name__)

@app.route('/process_form', methods=['POST'])
def process_form():
    nome_pet = request.form['nome_pet']
    local_visto = request.form['local_visto']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    fotos = request.files.getlist('fotos')
    nome_tutor = request.form['nome_tutor']
    email_tutor = request.form['email_tutor']
    telefone_tutor = request.form['telefone_tutor']
    
    # Faça o processamento dos dados aqui
    
    # Grava um log de todas as requisições recebidas
    with open('log.txt', 'a') as file:
        file.write(f'Nome do pet: {nome_pet}\n')
        file.write(f'Último local visto: {local_visto}\n')
        file.write(f'Latitude: {latitude}\n')
        file.write(f'Longitude: {longitude}\n')
        file.write(f'Fotos: {fotos}\n')
        file.write(f'Nome do tutor: {nome_tutor}\n')
        file.write(f'E-mail do tutor: {email_tutor}\n')
        file.write(f'Telefone do tutor: {telefone_tutor}\n\n')
    
    return 'Formulário recebido com sucesso!'

if __name__ == '__main__':
    app.run()
