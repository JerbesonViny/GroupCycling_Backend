from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey
import marshmallow as ma

from app.database.configuration import engine

Base = declarative_base()

# Classe/modelo de usuário
class User(Base):
  __tablename__ = "users"

  uuid = Column(String, primary_key=True)
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
  author_uuid = Column(Integer, ForeignKey("users.uuid"))

  def __repr__(self) -> str:
    return f"<Event(Title={self.title}, origin=[{self.origin_latitude}, {self.origin_longitude}], destination=[{self.destination_latitude}, {self.destination_longitude}])>"

class UserSchema(ma.Schema):
  class Meta:
    fields = ('uuid', 'name', 'email', 'password')

class EventSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'type_bike', 'meeting', 'intensity', 'type_route', 'origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude', 'author_uuid')

# Serializer User
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Serializer Event
event_schema = EventSchema()
events_schema = EventSchema(many=True)
