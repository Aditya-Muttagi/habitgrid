from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, habits
from app.db.base import templates

from fastapi.staticfiles import StaticFiles

#Starts the App
app = FastAPI(title="HabitGrid")

app.mount('/static', StaticFiles(directory='app/static'), name='static')

#Tells from which server to allow to modify the db,* means from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Add all these endpoints into main.py
app.include_router(auth.router)
app.include_router(habits.router)

@app.get("/")
async def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})