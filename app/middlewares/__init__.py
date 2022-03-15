from functools import wraps
from flask import jsonify, request
from app.utils.secury import decode_token

def authorization_is_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    authorization = request.headers

    # Se o token tiver sido passado pelos headers
    if( authorization.get('X-access-token') is None ):
      
      return jsonify(message="É necessário estar logado para ter acesso a essa funcionalidade!"), 401 # Unauthorized

    return f(*args, **kwargs)
  
  return decorated_function

def valid_token(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    authorization = request.headers

    # Se o token enviado é válido e pode ser decodificado
    if( decode_token(authorization.get('X-access-token')) is None ):
    
      return jsonify(message="Token inválido e/ou expirou!"), 401 # Unauthorized

    return f(*args, **kwargs)
  
  return decorated_function