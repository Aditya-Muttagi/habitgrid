def test_user_model_importable():
    # simple smoke test: importing the model should not raise
    from app.models.user import User
    assert getattr(User, "__tablename__", None) == "users"