from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Criando a engine que faz comunicação com o banco
engine = create_async_engine(os.environ.get('SQLALCHEMY_DATABASE_URL'), echo=True)

# Criando a sessão async
Session = sessionmaker(
    future=True,
    class_=AsyncSession
    bind=engine
)
