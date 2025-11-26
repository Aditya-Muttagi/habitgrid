from fastapi import APIRouter, Depends
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
    token: str = Depends(get_current_user)
):
    habit = Habit(user_id=token, name=payload.name)
    db.add(habit)
    await db.commit()
    await db.refresh(habit)
    return habit

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
