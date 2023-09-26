from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .config import SECRET_KEY
from .exception_handlers import unauthorized_handler

from .panel.router import panel_router
from .auth.router import auth_router


app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.mount("/static/panel/", StaticFiles(directory="static/panel"), name="panel_static")
app.mount("/static/auth/", StaticFiles(directory="static/auth"), name="auth_static")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.add_exception_handler(HTTPException, unauthorized_handler)

app.include_router(panel_router, tags=["panel"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])