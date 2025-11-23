from app.core.Pwd_hash_verify import hash_password, verify_password

def test_hash_and_verify_password():
    raw = "test123"
    hashed = hash_password(raw)
    assert hashed != raw  # should never store raw passwords
    assert verify_password(raw, hashed) is True
    assert verify_password("wrong", hashed) is False
