from pydantic import BaseModel

#Input Format-> payload
class HabitCreate(BaseModel):
    name: str

class HabitEntryUpdate(BaseModel):
    done: bool
