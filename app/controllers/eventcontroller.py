from app.database.configuration import Session
from app.database.schemas import Event
from sqlalchemy.future import select

# Função que permite a criação de novos eventos
async def create_event(event: Event) -> int:
  # Abrindo uma sessão no banco
  async with Session() as s:
    s.add( event )
    await s.commit()
    await s.refresh( event )

    return event.id

# Função que permite captar todos os eventos cadastrados
async def get_all_events() -> list:
  # Abrindo uma sessão no banco
  async with Session() as s:
    query = await s.execute(
      select(Event)
    ) # Selecionando todos os dados da tabela de eventos

    return query.scalars().all()

# Função que permite captar os eventos cadastrados por um usuário específico
async def get_events_per_user(user_uuid: str) -> list:
  # Abrindo uma sessão no banco
  async with Session() as s:
    query = await s.execute(
      select(Event).where(Event.author_uuid == user_uuid)
    ) # Selecionando todos os eventos que tenham sido criados pelo usuário informado

    return query.scalars().all()
