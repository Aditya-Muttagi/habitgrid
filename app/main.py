from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, habits

#Starts the App
app = FastAPI(title="HabitGrid")

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
