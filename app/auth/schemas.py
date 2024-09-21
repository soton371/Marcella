from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True

        
# for send otp
class TakeEmail(BaseModel):
    email: str

# for match otp
class MatchOtpPayload(BaseModel):
    email: str
    otp_code: str