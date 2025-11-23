from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "extra": "forbid"
    }
