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