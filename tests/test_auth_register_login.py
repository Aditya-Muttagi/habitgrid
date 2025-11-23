# tests/test_auth_register_login.py
import pytest

@pytest.mark.asyncio
async def test_register_and_login(async_client):
    email = "inttestuser@example.com"
    resp = await async_client.post("/api/v1/auth/register", json={"email": email, "password": "strongpass123"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == email
    assert "id" in body

    resp2 = await async_client.post("/api/v1/auth/login", json={"email": email, "password": "strongpass123"})
    assert resp2.status_code == 200
    token_body = resp2.json()
    assert "access_token" in token_body
    assert token_body["token_type"] == "bearer"