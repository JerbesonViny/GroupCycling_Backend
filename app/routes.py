from flask import request, jsonify,  url_for
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from io import BytesIO
from uuid import uuid4
import asyncio, base64, os

from app import app, oauth
from app.utils import search_arg
from app.utils.secury import create_token, decode_token
from app.utils.helpers import upload_file_to_s3, allowed_file
from app.controllers.usercontroller import create_user, verify_user_exists, authentication, search_by_uuid
from app.controllers.eventcontroller import create_event, get_all_events, get_events_per_user
from app.controllers.postcontroller import create_post, get_all_posts

from app.middlewares import authorization_is_required, valid_token

from app.database.schemas import ( 
  Post, User, Event, 
  user_schema,  events_schema, 
  post_schema, posts_schema )

loop = asyncio.get_event_loop()

@app.route('/')
def home():
  return jsonify(message='Hello')

@app.route('/login', methods=['POST',])
def login():
  data = request.json

  # Verificando se todos os campos foram preenchidos
  if( data.get('email') and data.get('password') ):
    auth = loop.run_until_complete(authentication(data['email'], data['password']))

    # Se existir um user com as credenciais que foram passadas
    if( auth is not None and len(auth) > 0 ):
      auth = user_schema.dump(auth)
      token = create_token(auth)

      return jsonify(token=token), 200 # OK

    return jsonify(message="E-mail e/ou senha incorretos!"), 400 # Bad Request

  return jsonify(message="Preencha todos os campos!"), 422 # Unprocessable Entity

@app.route('/google-auth')
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

@app.route('/user-info', methods=['GET',])
def get_info_user():
  authorization = request.headers

  if( authorization.get('X-access-token') is not None ):
    user_info = decode_token(authorization.get('X-access-token'))

    if( user_info is not None):
      data = {
        "name": user_info['name'],
        "email": user_info['email']
      }

      return jsonify(data)
    else:
      return jsonify(message="Token inválido!"), 400 # Bad Request
  else:
    return jsonify(message="X-access-token é obrigatório!"), 400 # Bad Request

@app.route('/register', methods=['POST',])
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

  return jsonify(message="Preencha todos os campos"), 422 # Unprocessable Entity

@app.route('/events/create', methods=['POST',])
def add_event():
  data = request.json
  authorization = request.headers

  if( authorization.get('X-access-token') is None ):
    return jsonify(message="É necessário estar logado para ter acesso a essa funcionalidade!"), 401 # Unauthorized
  else:
    payload = decode_token(authorization.get('X-access-token'))

    if( payload == None ):
      return jsonify(message="Token inválido e/ou expirou!"), 401 # Unauthorized

  # Verificando se todos os campos foram preenchidos
  if( data.get('title') and data.get('type_bike') and data.get('meeting') and data.get('intensity') and data.get('type_route') and data.get('origin') and data.get('destination') ):
    if( data.get('origin').get('latitude') and data.get('origin').get('longitude') and data.get('destination').get('latitude') and data.get('destination').get('longitude') ):
      event = Event(
        title=data.get('title'),
        type_bike=data.get('type_bike'),
        meeting=data.get('meeting'),
        intensity=data.get('intensity'),
        type_route=data.get('type_route'),
        origin_latitude=data.get('origin').get('latitude'),
        origin_longitude=data.get('origin').get('longitude'),
        destination_latitude=data.get('destination').get('latitude'),
        destination_longitude=data.get('destination').get('longitude'),
        author_uuid=payload['uuid']
      ) # Instânciando o evento

      try:
        event_id = loop.run_until_complete(create_event(event))

        return jsonify(event_id=event_id), 201 # Created
      except:
        return jsonify(message="Ocorreu um erro ao tentar cadastrar o evento!"), 400 # Bad Request

  return jsonify(message="Preencha todos os campos!"), 422 # Unprocessable Entity

@app.route('/events', methods=['GET',])
def list_events():
  authorization = request.headers

  # Se o token tiver sido passado pelos headers
  if( authorization.get('X-access-token') ):
    # Se o token enviado é válido e pode ser decodificado
    if( decode_token(authorization.get('X-access-token')) ):
      eventos = loop.run_until_complete(get_all_events()) # Captando todos os eventos
      eventos = events_schema.dump(eventos)

      return jsonify(eventos), 200 # OK

    return jsonify(message="Token inválido e/ou expirou!"), 401 # Unauthorized

  return jsonify(message="É necessário estar logado para ter acesso a essa funcionalidade!"), 401 # Unauthorized

@app.route('/search-events', methods=['GET', 'HEAD',])
def list_events_per_author():
  params = request.query_string # Obtendo os parâmetros passados via URL
  list_args = params.decode('UTF-8').split("=") # Dispondo os itens obtidos em um array
  uuid_pos = search_arg(list_args ,'author_uuid') # Procurando o argumento "author_uuid" nos parâmetros
  authorization = request.headers

  # Se o token tiver sido passado pelos headers
  if( authorization.get('X-access-token') ):
    # Se o token enviado é válido e pode ser decodificado
    if( decode_token(authorization.get('X-access-token')) ):
      # Verificando se foi possível encontrar o argumento "author_uuid" nos parâmetros passados
      if( uuid_pos is not None ):
        # O valor do argumento "author_uuid" está uma posição a frente do argumento
        uuid_values_pos = uuid_pos + 1
        events = loop.run_until_complete( get_events_per_user(list_args[uuid_values_pos]) )
      else:
        events = None

      events = events_schema.dump(events) # Serializando os dados obtidos    

      return jsonify(events), 200 # OK
    
    return jsonify(message="Token inválido e/ou expirou!"), 401 # Unauthorized

  return jsonify(message="É necessário estar logado para ter acesso a essa funcionalidade!"), 401 # Unauthorized

@app.route('/send-image/', methods=['POST',])
@authorization_is_required
@valid_token
def send_image():
  user_info = decode_token(request.headers['X-access-token'])

  # Verificando se o Base64 foi enviado
  if( "Base64" not in request.json ):
    return jsonify(message="FileImage is required!"), 422 # Unprocessable Entity
  
  # Captando o Base64
  files = request.json['Base64']

  # Verificando se o arquivo nao eh vazio
  if( files == "" ):
    return jsonify(message="No selected file"), 422 # Unprocessable Entity
  
  im = BytesIO(base64.b64decode(files)) # Decodificando o base64
  image_name = f"{uuid4().hex}{datetime.now().strftime('%Y%m%d')}.png" # Criando o nome da imagem
  output = upload_file_to_s3(file=im, path=os.environ.get('PATH_POSTS'), filename=image_name) # Tentando enviar a imagem para o AWS

  # Se o upload tiver sido efetuado com sucesso
  if output:
    user_identification = loop.run_until_complete(search_by_uuid(uuid=user_info['uuid']))

    if( user_identification is not None ):
      post = Post(
        caption   = request.json.get('caption'),
        image_url = f"{os.environ.get('PATH_POSTS')}/{image_name}",
        author_id = user_identification[0]
      )
      
      new_post = loop.run_until_complete(create_post(post))

      if( new_post is None ):
        return jsonify(message="Could not create post"), 400 # Bad Request
      
      return jsonify(message="Post created successfully"), 200 # OK
    else:
      return jsonify(message="Invalid token and/or expired"), 401 # Unauthorized

  else:
    return jsonify(message="Unable to upload, try again"), 400 # Bad Request
      
@app.route('/posts', methods=['GET',])
@authorization_is_required
@valid_token
def get_posts():
  posts = loop.run_until_complete(get_all_posts())

  return jsonify(posts_schema.dump(posts))