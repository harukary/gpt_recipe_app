from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
