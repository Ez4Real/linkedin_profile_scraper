import bcrypt
from pydantic import EmailStr

from database import user_collection

from .models import User


async def get_user_by_email(email: EmailStr):
    return await user_collection.find_one({"email": email})

async def create_user(email: EmailStr, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(email=email, hashed_password=hashed_password)
    return await user_collection.insert_one(dict(user))