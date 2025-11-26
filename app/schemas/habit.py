from pydantic import BaseModel

#Input Format-> payload
class HabitCreate(BaseModel):
    name: str
    class Config:
        extra = "ignore"

class HabitEntryUpdate(BaseModel):
    done: bool
