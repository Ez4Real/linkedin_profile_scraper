from typing import List

from fastapi import Request, Response
from passlib.context import CryptContext

from config import DEBUG


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def set_secure_cookie(response: Response, key: str, value: str) -> None:
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=not DEBUG,
        samesite='lax'
    )


def set_error_message(request: Request, message: str) -> None:
    request.session['error_message'] = message
    
def set_error_messages(request: Request, messages: List) -> None:
    request.session['error_messages'] = messages


def set_success_message(request: Request, message: str) -> None:
    request.session['success_message'] = message
    

def pop_get_error_message(request: Request) -> None:
    return request.session.pop('error_message', None)

def pop_get_error_messages(request: Request) -> None:
    return request.session.pop('error_messages', None)


def pop_get_success_message(request: Request) -> None:
    return request.session.pop('success_message', None)