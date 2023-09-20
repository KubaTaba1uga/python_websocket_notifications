from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from .database import Base


class User(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    from_ = Column(Integer, ForeignKey("user.id"), name="from_", key="from")
    to = Column(Integer, ForeignKey("user.id"), name="to_")