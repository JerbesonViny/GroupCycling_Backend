import hashlib

# Função que permite criptografar de dados
def encrypt_data(data: str) -> str:
    hash = hashlib.sha512() # Selecionando o método criptográfico
    hash.update(data.encode('UTF-8')) # Criptografando a informação

    return hash.hexdigest() # Retornando a informação criptografada
