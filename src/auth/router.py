from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .models import UserSignUp
from .security import create_access_token, create_refresh_token
from .service import create_user, get_user_by_email
from .utils import (pop_get_error_message, pop_get_error_messages,
                    pop_get_success_message, set_error_message,
                    set_error_messages, set_secure_cookie, set_success_message,
                    verify_password)

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
            refresh_token = create_refresh_token(email)
            response = RedirectResponse(url='/', status_code=302)
            set_secure_cookie(response, "Authorization", f"Bearer {access_token}")
            set_secure_cookie(response, "RefreshToken", refresh_token)
            return response
            
    return LOGIN_REDIRECT



# @auth_router.post('/refresh-token')
# async def refresh_token(request: Request):
#     refresh_token = request.cookies.get("RefreshToken")
#     new_access_token = get_new_access_token(refresh_token)
#     response = RedirectResponse(url='/', status_code=302)
#     set_secure_cookie(response, "Authorization", f"Bearer {new_access_token}")
#     return response


@auth_router.get('/logout')
async def logout(response: RedirectResponse):
    response = LOGIN_REDIRECT
    response.delete_cookie('Authorization')
    response.delete_cookie('RefreshToken')
    return response