from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session

from .database import Base


class User(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    from_ = Column(Integer, ForeignKey("app_user.id"), name="from_", key="from")
    to = Column(Integer, ForeignKey("app_user.id"), name="to_")


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(User).offset(skip).limit(limit).all()


def save_obj(db: Session, obj: Base):
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj
