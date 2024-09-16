from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    email: str
    full_name: str | None = None

    class Config:
        orm_mode = True

        