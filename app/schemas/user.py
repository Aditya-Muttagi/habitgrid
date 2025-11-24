from pydantic import BaseModel, EmailStr

#Used as Input format in auth.py
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Used as Input format in auth.py
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Checks the validity of Id and the Email
class UserRead(BaseModel):
    id: int
    email: EmailStr
