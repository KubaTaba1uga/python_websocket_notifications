from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session

from .database import Base
from .schemas import MessageUserSchema


class User(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    from_ = Column(Integer, ForeignKey("app_user.id"), name="from_")
    to = Column(Integer, ForeignKey("app_user.id"), name="to_")


def get_user(db: Session, user_id: int) -> User:
    return _get_class_by_id(db, User, user_id)


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list:
    return _list_class(db, User, skip, limit)


def get_message(db: Session, msg_id: int) -> Message:
    return _get_class_by_id(db, Message, msg_id)


def list_messages(db: Session, skip: int = 0, limit: int = 100) -> list:
    return _list_class(db, Message, skip, limit)


def create_messge(db: Session, message: MessageUserSchema) -> Message:
    return Message(from_=message.from_, to=message.to, content=message.content)


def save_obj(db: Session, obj: Base) -> None:
    db.add(obj)
    db.commit()
    db.refresh(obj)


def _get_class_by_id(db, class_, id_):
    return db.query(class_).filter(class_.id == id_).first()


def _list_class(db, class_, skip, limit):
    return db.query(class_).offset(skip).limit(limit).all()
