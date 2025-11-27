from fastapi import APIRouter
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.habit import Habit, HabitEntry
from app.schemas.habit import HabitCreate, HabitEntryUpdate
from app.core.jwt import decode_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

router = APIRouter(prefix="/habits", tags=["habits"])

#Returns token if it has Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        return int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

@router.post("/")
async def create_habit(
    payload: HabitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    q = await db.execute(select(Habit).where(Habit.user_id == current_user, Habit.name == payload.name))
    existing = q.scalars().first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already have a habit with this name.")
    habit = Habit(user_id=current_user, name=payload.name)
    db.add(habit)
    await db.commit()
    await db.refresh(habit)
    return habit

@router.delete("/{habit_id}")
async def delete_habit(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    token: int = Depends(get_current_user)
):
    res = await db.execute(select(Habit).where(Habit.id == habit_id, Habit.user_id == token))
    habit = res.scalars().first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    await db.delete(habit)
    await db.commit()
    return {"detail": "Habit deleted"}

@router.post("/{habit_id}/today")
async def update_today(habit_id: int, payload: HabitEntryUpdate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(HabitEntry).where(HabitEntry.habit_id == habit_id))
    entry = q.scalars().first()

    if not entry:
        entry = HabitEntry(habit_id=habit_id, done=payload.done)
        db.add(entry)
    else:
        entry.done = payload.done

    await db.commit()
    return {"habit_id": habit_id, "done": payload.done}

@router.get("/today")
async def get_today(
    db: AsyncSession = Depends(get_db),
    token: int = Depends(get_current_user)
):
    q = await db.execute(select(Habit).where(Habit.user_id == token))
    habits = q.scalars().all()

    q2 = await db.execute(select(HabitEntry))
    entries = {e.habit_id: e.done for e in q2.scalars().all()}

    return [
        {"habit_id": h.id, "name": h.name, "done": entries.get(h.id, False)}
        for h in habits
    ]
