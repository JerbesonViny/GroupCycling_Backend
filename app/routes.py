from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
import asyncio

from app import app
from app.database.schemas import User
from app.controllers.usercontroller import create_user

loop = asyncio.get_event_loop()

@app.route('/')
def home():
    return 'Hello'

@app.route('/register/', methods=['POST',])
def create_account():
    data = request.json

    # Verificando se todos os campos foram preenchidos
    if( data.get('name') and data.get('email') and data.get('password') and data.get('password_again') ):
        if( data.get('password') == data.get('password_again') ):
            # Criando uma instância do usuário
            new_user = User(name=data['name'], email=data['email'], password=data['password'])

            try: # tentando criar o usuário
                user_uuid = loop.run_until_complete( create_user(new_user) )

                return jsonify(user_uuid=user_uuid), 201 # Created
            except IntegrityError: # Erro de integridade
                return jsonify(message="Esse e-mail já está em uso, tente novamente utilizando outro!"), 400 # Bad Request

        return jsonify(message="As senhas não coincidem, tente novamente!"), 400 # Bad Request

    return jsonify(message="Preencha todos os campos"), 400 # bad Request
