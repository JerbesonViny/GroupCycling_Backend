from flask import request, jsonify, redirect, url_for
from sqlalchemy.exc import IntegrityError
import asyncio

from app import app, oauth, google
from app.utils.secury import create_token
from app.database.schemas import ( 
    User, user_schema, users_schema
)
from app.controllers.usercontroller import ( 
    create_user, verify_user_exists, authentication
)

loop = asyncio.get_event_loop()

@app.route('/')
def home():
    return jsonify(message='Hello')

@app.route('/login/', methods=['POST',])
def login():
    data = request.json

    # Verificando se todos os campos foram preenchidos
    if( data.get('email') and data.get('password') ):
        auth = loop.run_until_complete(authentication(data['email'], data['password']))

        if( auth is not None and len(auth) > 0 ):
            auth = user_schema.dump(auth)
            token = create_token(auth)

            return jsonify(token=token), 200 # OK
        
        return jsonify(message="E-mail e/ou senha incorretos!"), 400 # Bad Request

    return jsonify(message="Preencha todos os campos!"), 400 # Bad Request
    
@app.route('/google-auth/')
def google_auth():
    google = oauth.create_client('google') # Abrindo uma tela do google, onde o usuário poderá se autenticar a partir dele
    redirect_uri = url_for('authorize', _external=True) # Criando uma URL para redirecionar o usuário
    return google.authorize_redirect(redirect_uri) # Após ser autenticado, redirecionar o usuário para a URL anteriormente definida

@app.route('/authorize')
def authorize():
    google = oauth.create_client("google") # Abrindo uma tela do google, onde o usuário poderá se autenticar a partir dele
    token = google.authorize_access_token() # Captando o token após o usuário ser autenticado
    resp = google.get('userinfo') # Captando as informações do usuário. Ex: DisplayName: 'Maria'
    user_info = resp.json() # Transformando as informações em um JSON e armazenando-as na variável "user_info"

    # Verificando se o usuário não existe
    if( loop.run_until_complete(verify_user_exists(user_info['email'])) == False ):
        new_user = User(
            name=user_info['name'],
            email=user_info['email'],
            password=user_info['id']
        )

        # Caso ele não exista, criar o mesmo
        loop.run_until_complete(create_user(new_user))

    user_credentials = {"email": user_info["email"]}
    token = create_token(user_credentials)

    return jsonify(token=token)


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
