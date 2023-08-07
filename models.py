from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    hashed_password: str

class UserInDB(UserCreate):
    _id: str