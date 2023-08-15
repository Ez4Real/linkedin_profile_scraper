from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .models import User
from .schemas import user_serializer
from bson import ObjectId
from database import user_collection


auth_router = APIRouter()

templates = Jinja2Templates(directory="templates/auth")

@auth_router.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})

@auth_router.post("/signup")
async def signup_post(request: Request,
                      email: str = Form(...),
                      password: str = Form(...)):
    if request.method == "POST":
        user = User(email=email, hashed_password=password)
        result = await user_collection.insert_one(dict(user))
        
        print('\n', result)
        
        inserted_id = result.inserted_id
        inserted_user = await user_collection.find_one({"_id": inserted_id})
        user_data = user_serializer(inserted_user)
        return {
            "message": "User has been successfully created",
            "user_data": user_data
        }
    return templates.TemplateResponse("sign_up.html", {"request": request})

@auth_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
