from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey
import marshmallow as ma

Base = declarative_base()

# Classe/modelo de usuário
class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, autoincrement=True)
  uuid = Column(String, unique=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(Text, nullable=False)

  def __repr__(self) -> str:
    return f"<User(Email={self.email})>"

# Modelo de evento
class Event(Base):
  __tablename__ = "events"

  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(30), nullable=False)
  type_bike = Column(String, nullable=False)
  meeting = Column(String, nullable=False)
  intensity = Column(String, nullable=False)
  type_route = Column(String, nullable=False)
  origin_latitude = Column(Float, nullable=False)
  origin_longitude = Column(Float, nullable=False)
  destination_latitude = Column(Float, nullable=False)
  destination_longitude = Column(Float, nullable=False)
  author_id = Column(Integer, ForeignKey("users.id"))

  def __repr__(self) -> str:
    return f"<Event(Title={self.title}, Origin=[{self.origin_latitude}, {self.origin_longitude}], Destination=[{self.destination_latitude}, {self.destination_longitude}])>"


class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, autoincrement=True)
  caption = Column(String(250), nullable=False)
  image_url = Column(Text, nullable=False)
  author_id = Column(Integer, ForeignKey("users.id"))

  def __repr__(self) -> str:
    return f"<Posts(Caption={self.caption}, ImageUrl={self.image_url}, Author={self.author_id})>"

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'uuid', 'name', 'email', 'password')

class EventSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'type_bike', 'meeting', 'intensity', 'type_route', 'origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude', 'author_id')

class PostSchema(ma.Schema):
  class Meta:
    fields = ('id', 'caption', 'image_url', 'author_id')

# Serializer User
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Serializer Event
event_schema = EventSchema()
events_schema = EventSchema(many=True)

# Serializer Post
post_schema = PostSchema()
posts_schema = PostSchema(many=True)