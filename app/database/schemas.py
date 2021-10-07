from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column
import marshmallow as ma

from app.database.configuration import engine

Base = declarative_base()

# Classe/modelo de usuário
class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"<User(Email={self.email})>"

class UserSchema(ma.Schema):
    class Meta:
        fields = ('uuid', 'name', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)