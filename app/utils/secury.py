import hashlib, jwt, os
from datetime import timedelta, datetime

# Função que permite criptografar de dados
def encrypt_data(data: str) -> str:
  hash = hashlib.sha512() # Selecionando o método criptográfico
  hash.update(data.encode('UTF-8')) # Criptografando a informação

  return hash.hexdigest() # Retornando a informação criptografada

# Função de criar token
def create_token(data: dict) -> str:
  # Adicionando um tempo de expiração
  data["exp"] = datetime.utcnow() + timedelta(hours=1)

  return jwt.encode(payload=data, key=os.environ.get('SECRET_KEY'), algorithm="HS256")

# Função para decoficar o token
def decode_token(token: str) -> dict:
  # Tentando decodificar o token
  try:
    decoded_token = jwt.decode(jwt=token, key=os.environ.get("SECRET_KEY"), algorithms=["HS256"])
  except:
    return None

  return decoded_token
