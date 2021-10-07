import uuid
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
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

            raise IntegrityError("Exists", "Email", "User") # Retornar None

        return user.uuid # Retornando o UUID do usuário cadastrado

# Função para verificar se o usuário existe no sistema
async def verify_user_exists(email: str) -> bool:
    # Abrindo uma sessão no banco
    async with Session() as s:
        query = await s.execute(
            select(User.uuid).where(User.email == email)
        ) # Retornando o uuid do usuário que possui o email igual ao que foi passado

        # Se algo tiver sido retornado
        if( query.first() ):
            return True

        return False # Caso contrário, não existe esse usuário