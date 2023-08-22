from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from auth.security import get_current_user

panel_router = APIRouter()

templates = Jinja2Templates(directory="templates/panel")

@panel_router.get("/", response_class=HTMLResponse)
async def panel(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("panel.html", {"request": request, "current_user": user['email']})