import asyncio # Pacote que permite executar funções async

from app.database.configuration import engine
from app.database.schemas import Base

# Função de criação das tabelas no banco
async def create_tables():
    # Iniciando a engine e criando uma conexão com o banco
    async with engine.begin() as conn:
        # Esperando todas as tabelas do banco serem apagadas
        await conn.run_sync(Base.metadata.drop_all)
        # Esperando todas as tabelas do banco serem criadas
        await conn.run_sync(Base.metadata.create_all)
