from pydantic import BaseModel


class DbModel:
    class Config:
        orm_mode = True


class UserSchema(BaseModel, DbModel):
    id: int
    username: str


class MessageUserSchema(BaseModel, DbModel):
    from_: int
    to: int
    content: str


class MessageServerSchema(MessageUserSchema):
    id: int
