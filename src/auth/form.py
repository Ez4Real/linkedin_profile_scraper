import re
from typing import List

from fastapi import Request
from pydantic import EmailStr

from config import ALLOWED_EMAIL_DOMAINS


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: EmailStr
        self.password: str

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get('email')
        self.password = form.get('password')
    
    def is_valid(self):
        if self.email.split('@')[1] not in ALLOWED_EMAIL_DOMAINS:
            self.errors.append('Email must belong to Vichinth company domain')
        if len(self.password) < 8:
            self.errors.append('Password must be at least 8 characters long')
        if not re.match(
                r'^(?=.*[A-Za-z])[A-Za-z0-9!@#$%^&*()_+{}:;<>,.?~\-+=|\[\]\\\/]+$',
                self.password
            ):
            self.errors.append('Password can only contain letters (at least 1), digits, and special symbols')
        return False if self.errors else True