from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

#Class Inheritance, Base knows the structure and stores metadata of the Table
class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)

class HabitEntry(Base):
    __tablename__ = "habit_entries"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    date = Column(Date, server_default=func.current_date())
    done = Column(Boolean, default=False)
