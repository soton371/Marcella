from sqlalchemy import Column, Integer, String

from core.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    password = Column(String)


class OtpStore(Base):
    __tablename__ = "otp_store"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    otp = Column(String, nullable=True)
    send_time = Column(String, nullable=True)