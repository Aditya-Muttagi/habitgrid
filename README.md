## HabitGrid

A simple habit-tracking application built with **FastAPI**, **SQLAlchemy (async)**, and a minimal HTML/JS frontend. Users can register, log in, and manage daily habits through a clean API and simple web interface.

---

### Features

 - User registration and login (bcrypt + JWT)

 - Create and manage habits

 - View today’s habits

 - Mark habits as completed

 - Async FastAPI backend

 - Lightweight static frontend (HTML + JS + CSS)

 - PostgreSQL 

 - Async pytest test suite

---

### Project Structure

```txt
app/
├── api
│   └── v1
│       ├── auth.py
│       └── habits.py
├── core
│   ├── jwt.py
│   ├── security.py
│   └── config.py
├── crud
│   ├── user.py
│   └── habit.py
├── db
│   ├── base.py
│   └── session.py
├── models
│   ├── user.py
│   └── habit.py
├── schemas
│   ├── user.py
│   └── habit.py
└── main.py

static/
├── index.html
├── login.html
├── register.html
├── habits.html
├── app.js
└── styles.css

tests/
├── test_auth.py
├── test_habits.py
└── conftest.py
```

---

### How to Run

 - Install dependencies:

``` pip install -r requirements.txt ```


 - Start the server:

```uvicorn app.main:app --reload```


 - Open in browser:

```API docs: http://127.0.0.1:8000/docs```

```Frontend: http://127.0.0.1:8000/```

 - Run Tests:

```pytest```
