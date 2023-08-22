from fastapi import APIRouter, Request, Depends, HTTPException, status, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from config import DEBUG

from .service import create_user, get_user_by_email
from .schemas import TokenSchema
from .utils import  verify_password, create_access_token, create_refresh_token
from .models import UserSignUp


auth_router = APIRouter()
templates = Jinja2Templates(directory='templates/auth')


@auth_router.get('/signup', response_class=HTMLResponse)
async def get_signup(request: Request):
    messages = request.session.pop('error_messages', None)
    
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
        request.session['error_messages'] = ['User with this email already exists']
    else:
        try:
            UserSignUp(email=email, password=password)
        except ValueError as e:
            error_messages = [error['msg'] for error in e.errors()]
            request.session['error_messages'] = error_messages
        else:
            await create_user(email, password)
            request.session['success_message'] = 'User registration successful'
            return RedirectResponse(url='/auth/login', status_code=status.HTTP_302_FOUND)

    return RedirectResponse(url='/auth/signup', status_code=status.HTTP_302_FOUND)


@auth_router.get('/login', response_class=HTMLResponse)
async def get_login(request: Request,
                    message: str = None):
    error_message = request.session.pop('error_message', None)
    if not error_message:
        message = request.session.pop('success_message', None)
        
    return templates.TemplateResponse(
        'login.html',
        {'request': request, 'message': message, 'error_message': error_message}
    )
    

# @auth_router.post('/login')
# async def post_login(request: Request,
#                      email: str = Form(...),
#                      password: str = Form(...)):
#     user = await get_user_by_email(email)
#     if not user:
#         request.session['error_message'] = 'User with this e-mail address does not exist'
#     else:
#         if not verify_password(password, user['hashed_password']):
#             request.session['error_message'] = 'Incorrect email or password'
#         else: 
#             access_token = create_access_token(email)
#             response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
#             response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
#             return response
            
#     return RedirectResponse(url='/auth/login', status_code=status.HTTP_302_FOUND)


@auth_router.post('/login', response_model=TokenSchema)
async def post_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email'
        )

    if not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect password'
        )
        
    return {
        'access_token': create_access_token(user['email']),
        'refresh_token': create_refresh_token(user['email']),
    }