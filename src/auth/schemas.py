from pydantic import BaseModel


def user_serializer(user) -> dict:
    return {
        'id': str(user['_id']),
        'email': user['email'],
    }
    

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None