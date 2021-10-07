import uuid, asyncio

from app.database.configuration import Session
from app.utils.secury import encrypt_data
from app.database.schemas import User

# Função que permite criar usuários
async def create_user(user: User) -> str:
    user.password = encrypt_data(user.password)
    user.uuid = uuid.uuid4()

    # Abrindo uma sessão no banco
    async with Session() as s:
        try: # Tentando
            s.add(user) # Adicionar usuário ao banco
            await s.commit() # Confirmando as alterações
            await s.refresh(user) # Recarregando os dados do usuário
        except: # Caso haja uma exceção
            await s.rollback() # Desfazer as alterações

            return None # Retornar None

        return user.uuid # Retornando o UUID do usuário cadastrado
