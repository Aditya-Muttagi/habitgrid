from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, habits
from fastapi.staticfiles import StaticFiles

#Starts the App
app = FastAPI(
    title="HabitGrid",
    swagger_ui_favicon_url="/favicon.png",  # use the same favicon for /docs
)

#Add all these endpoints into main.py
app.include_router(auth.router)
app.include_router(habits.router)

#Tells from which external frontend or website are allowed to make request to the backend, * means from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Makes all the HTML files available at the path /..
app.mount("/", StaticFiles(directory="static", html=True), name="static")
