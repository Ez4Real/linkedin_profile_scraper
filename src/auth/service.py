from pydantic import EmailStr

from database import user_collection

from .models import UserInDB
from .utils import hash_password


async def get_user_by_email(email: EmailStr):
    return await user_collection.find_one({"email": email})

async def get_user_by_id(id: str):
    return await user_collection.find_one({"_id": id})

async def create_user(email: EmailStr, password: str):
    user = UserInDB(email=email, hashed_password=hash_password(password))
    return await user_collection.insert_one(dict(user))