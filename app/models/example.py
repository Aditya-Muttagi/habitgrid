from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
