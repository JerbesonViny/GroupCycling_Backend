from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

CORS(app, resources={r'/*': {'origin': '*'}})

oauth = OAuth(app) # Iniciando o OAuth2 a partir do app anteriormente criado
google = oauth.register(
  name="google",
  client_id='606410079738-7oh00tptc9mcjr9dpenevug4uqb3ah3f.apps.googleusercontent.com',
  client_secret='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',
  access_token_url="https://accounts.google.com/o/oauth2/token",
  acess_token_params=None,
  authorize_url="https://accounts.google.com/o/oauth2/auth",
  authorize_params=None,
  api_base_url="https://www.googleapis.com/oauth2/v1/",
  client_kwargs={"scope": "openid profile email"},
) # Definindo as configurações do OAuth2 [Isso não precisa ser explicado, pois, pega no google!]

from app.routes import *
