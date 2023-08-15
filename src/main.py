from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from config import SECRET_KEY

from panel.router import panel_router
from auth.router import auth_router

app = FastAPI()

app.mount("/static/panel/", StaticFiles(directory="static/panel"), name="panel_static")
app.mount("/static/auth/", StaticFiles(directory="static/auth"), name="auth_static")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(panel_router, tags=["panel"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])