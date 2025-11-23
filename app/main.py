from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth as auth_router

def create_app() -> FastAPI:
    app = FastAPI(title="HabitGrid")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router.router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app

app = create_app()
