# tests/test_auth.py
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.main import app as fastapi_app
from app.models.user import User
from tests.conftest import AsyncSessionLocal

# Import your real hash_password helper
from app.core.security import hash_password   # <-- IMPORTANT: adjust path if needed


async def _create_test_user(email: str, password: str):
    """Create a test user using the real bcrypt hashing."""
    async with AsyncSessionLocal() as session:
        user = User(
            email=email,
            hashed_password=hash_password(password)
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest.mark.asyncio
async def test_login_and_access_with_token(client: AsyncClient, clear_overrides):
    test_email = "testuser@example.com"
    test_password = "mypassword123"

    # create user row in test DB
    await _create_test_user(test_email, test_password)

    # Login using JSON payload that matches UserLogin(email, password)
    r = await client.post(
        "/auth/login",
        json={"email": test_email, "password": test_password},
    )
    assert r.status_code == 200, f"login failed: {r.status_code} {r.text}"
    body = r.json()
    assert "access_token" in body and "token_type" in body
    token = body["access_token"]

    # protected endpoint should reject without token
    r_no = await client.get("/habits/today")
    assert r_no.status_code in (401, 403)

    # protected endpoint with valid token
    r_ok = await client.get("/habits/today", headers={"Authorization": f"Bearer {token}"})
    assert r_ok.status_code == 200
    data = r_ok.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_invalid_token_is_rejected(client: AsyncClient, clear_overrides):
    res = await client.get("/habits/today", headers={"Authorization": "Bearer BADTOKEN"})
    assert res.status_code in (401, 403)
