from sqlalchemy import Column, Integer, String
from app.db.base import Base

#Class Inheritance
class User(Base):
    __tablename__ = "users"

    #Columns stored in users table in db
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
