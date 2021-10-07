from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

oauth = OAuth(app) # Iniciando o OAuth2 a partir do app anteriormente criado
google = oauth.register(
  name="google",
  client_id='1091356976572-h11ha06kpp4l50vghkpc70di7jnk5a3q.apps.googleusercontent.com',
  client_secret='kSiQj_RclyCg_XUVWcRN_jjr',
  access_token_url="https://accounts.google.com/o/oauth2/token",
  acess_token_params=None,
  authorize_url="https://accounts.google.com/o/oauth2/auth",
  authorize_params=None,
  api_base_url="https://www.googleapis.com/oauth2/v1/",
  client_kwargs={"scope": "openid profile email"},
) # Definindo as configurações do OAuth2 [Isso não precisa ser explicado, pois, pega no google!]

from app.routes import *
