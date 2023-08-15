from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

panel_router = APIRouter()

templates = Jinja2Templates(directory="templates/panel")

@panel_router.get("/", response_class=HTMLResponse)
async def panel(request: Request):
    user = request.session.get("user")
    # if not user:
    #     return RedirectResponse(url="auth/login")
    return templates.TemplateResponse("panel.html", {"request": request, "user": user})