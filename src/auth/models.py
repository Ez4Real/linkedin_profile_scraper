import re

from pydantic import BaseModel, EmailStr, SecretStr, Field, validator

from config import ALLOWED_EMAIL_DOMAINS

class UserSignUp(BaseModel):
    email: EmailStr = Field(...)
    password: SecretStr = Field(...)
    
    @validator('email')
    def validate_email(cls, value):
        if value.split('@')[1] not in ALLOWED_EMAIL_DOMAINS:
            raise ValueError('Email must belong to your company domain')
        return value

    @validator('password')
    def validate_password_length(cls, value):
        if not 7 < len(value) < 25:
            raise ValueError('Password must be between 8 and 24 characters long')
        return value

    @validator('password')
    def validate_password_characters(cls, value):
        if not re.match(r'^(?=.*[A-Za-z])[A-Za-z0-9!@#$%^&*()_+{}:;<>,.?~\-+=|\[\]\\\/]+$', value):
            raise ValueError('Password can only contain letters (at least 1), digits, and special symbols')
        return value

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str