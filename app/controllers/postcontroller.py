from app.database.configuration import Session
from app.database.schemas import Post
from sqlalchemy.future import select

# Funcao que permite criar posts
async def create_post(post: Post) -> int:
  # Abrindo uma sessao no banco
  async with Session() as s:
    try: # Tentando fazer a insercao do post no banco
      s.add( post )
      await s.commit()
      await s.refresh( post )

      return post.id
    except:
      return None