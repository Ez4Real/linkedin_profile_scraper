from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import DEBUG

from .service import create_user, get_user_by_email
from .utils import (verify_password,
                    set_success_message, 
                    set_error_message, set_error_messages,
                    pop_get_error_message, pop_get_error_messages,
                    pop_get_success_message)
from .security import create_access_token
from .models import UserSignUp


auth_router = APIRouter()
templates = Jinja2Templates(directory='templates/auth')


LOGIN_REDIRECT = RedirectResponse(url='/auth/login', status_code=302)


@auth_router.get('/signup', response_class=HTMLResponse)
async def get_signup(request: Request):
    messages = pop_get_error_messages(request)
    
    return templates.TemplateResponse(
        'sign_up.html',
        {'request': request, 'messages': messages}
    )

@auth_router.post('/signup')
async def post_signup(request: Request,
                      email: str = Form(...),
                      password: str = Form(...)):
    existing_user = await get_user_by_email(email)
    
    if existing_user:
        set_error_messages(request, ['User with this email already exists'])
    else:
        try:
            UserSignUp(email=email, password=password)
        except ValueError as e:
            set_error_messages(request, [error['msg'] for error in e.errors()])
        else:
            await create_user(email, password)
            set_success_message(request, 'User successfully created')
            return LOGIN_REDIRECT

    return RedirectResponse(url='/auth/signup', status_code=302)


@auth_router.get('/login', response_class=HTMLResponse)
async def get_login(request: Request,
                    message: str = None):
    error_message = pop_get_error_message(request)
    if not error_message:
        message = pop_get_success_message(request)
        
    return templates.TemplateResponse(
        'login.html',
        {'request': request, 'message': message, 'error_message': error_message}
    )

@auth_router.post('/login')
async def post_login(request: Request,
                     email: str = Form(...),
                     password: str = Form(...)):
    user = await get_user_by_email(email)
    if not user:
        set_error_message(request, 'User with this e-mail address does not exist')
    else:
        if not verify_password(password, user['hashed_password']):
            set_error_message(request, 'Incorrect email or password')
        else: 
            access_token = create_access_token(email)
            response = RedirectResponse(url='/', status_code=302)
            response.set_cookie(
                key="Authorization",
                value=f"Bearer {access_token}",
                httponly=True,
                secure=not DEBUG,
                samesite='lax'
            )
            return response
            
    return LOGIN_REDIRECT


@auth_router.get('/logout')
async def logout(request: Request):
    response = LOGIN_REDIRECT
    response.delete_cookie('Authorization')
    return response