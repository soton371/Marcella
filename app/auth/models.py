from sqlalchemy import Column, Integer, String

from core.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    password = Column(String)


