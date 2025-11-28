import pytest
from httpx import AsyncClient

from app.models.habit import Habit, HabitEntry
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_and_get_habits(client: AsyncClient, init_test_db):
    # create a habit (uses dependency override get_current_user -> user_id 1)
    payload = {"name": "Drink Water"}
    r = await client.post("/habits/", json=payload)
    assert r.status_code == 200 or r.status_code == 201
    data = r.json()
    assert data.get("name") == "Drink Water"
    habit_id = data.get("id") or data.get("habit_id") or data.get("id")

    # call GET /habits/today to ensure the new habit shows up with done=False
    r2 = await client.get("/habits/today")
    assert r2.status_code == 200
    array = r2.json()
    # find our habit
    found = [h for h in array if h.get("name") == "Drink Water"]
    assert len(found) == 1
    assert found[0]["done"] is False


@pytest.mark.asyncio
async def test_toggle_today_entry(client: AsyncClient, init_test_db):
    # create a habit to toggle
    payload = {"name": "Test Toggle"}
    r = await client.post("/habits/", json=payload)
    assert r.status_code in (200,201)
    habit = r.json()
    habit_id = habit.get("id")

    # Initially, GET /habits/today should show done False
    r = await client.get("/habits/today")
    assert r.status_code == 200
    items = r.json()
    h = next((it for it in items if it["name"] == "Test Toggle"), None)
    assert h is not None and h["done"] is False

    # POST toggle to mark done = true
    r2 = await client.post(f"/habits/{habit_id}/today", json={"done": True})
    assert r2.status_code == 200
    data = r2.json()
    assert data["done"] is True

    # GET again to confirm
    r3 = await client.get("/habits/today")
    items = r3.json()
    h = next((it for it in items if it["name"] == "Test Toggle"), None)
    assert h is not None and h["done"] is True
