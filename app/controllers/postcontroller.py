from app.database.configuration import Session
from app.database.schemas import Post
from sqlalchemy.future import select

# This function allow create new posts
async def create_post(post: Post) -> int:
  # Creating connection in BD
  async with Session() as s:
    try: # Try create new post
      s.add( post )
      await s.commit()
      await s.refresh( post )

      return post.id
    except:
      return None

# This function allow get all posts created
async def get_all_posts() -> list:
  # Creating connection in BD
  async with Session() as s:
    query = await s.execute(
      select(Post)
    ) # Select all posts

    return query.scalars().all()