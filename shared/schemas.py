from pydantic import BaseModel


class DbModel:
    class Config:
        orm_mode = True


class UserSchema(BaseModel, DbModel):
    id: int
    username: str


class MessageSchema(BaseModel, DbModel):
    id: int
    from_: int
    to: int
    content: str
