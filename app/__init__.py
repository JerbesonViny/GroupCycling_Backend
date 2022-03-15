from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os
import boto3

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

blueprint_swaggerui = get_swaggerui_blueprint(
  base_url='/docs',
  api_url='/static/openapi.yaml',
  config={
    "app_name": "Group Cycling"
  }
)

app.register_blueprint(blueprint_swaggerui)

CORS(app, resources={r'/*': {'origin': '*'}})

oauth = OAuth(app) # Iniciando o OAuth2 a partir do app anteriormente criado
google = oauth.register(
  name="google",
  client_id=os.environ.get('GOOGLE_CLIENT_ID'),
  client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
  access_token_url="https://accounts.google.com/o/oauth2/token",
  acess_token_params=None,
  authorize_url="https://accounts.google.com/o/oauth2/auth",
  authorize_params=None,
  api_base_url="https://www.googleapis.com/oauth2/v1/",
  client_kwargs={"scope": "openid profile email"},
) # Definindo as configurações do OAuth2 [Isso não precisa ser explicado, pois, pega no google!]

client = boto3.client(
  service_name='s3',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
  region_name='eu-west-1'
) # Configuração do AWS S3

from app.routes import *
