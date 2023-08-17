
from datetime import timedelta
from bson import ObjectId

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from config import ACCESS_TOKEN_EXPIRE_MINUTES

from .form import UserCreateForm
from .service import create_user, get_user_by_email
from .security import oauth2_scheme, create_access_token, verify_token


auth_router = APIRouter()
templates = Jinja2Templates(directory="templates/auth")


@auth_router.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})

@auth_router.post("/signup", response_class=HTMLResponse)
async def post_signup(request: Request):
    form = UserCreateForm(request)
    await form.load_data()
    
    if await get_user_by_email(form.email):
        form.errors.append('Email error, this Email id already in use')
    elif form.is_valid():
        result = await create_user(form.email, form.password)
        # if result.acknowledged:
        #     return RedirectResponse(url='/')
        
    return templates.TemplateResponse(
        "sign_up.html",
        {"request": request, "error_messages": form.errors}
    )


@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(form_data.username)
    if user and verify_token(form_data.password, user["hashed_password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})