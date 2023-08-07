from fastapi import FastAPI, Request, responses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routes import panel


app = FastAPI()

app.mount("/static/", StaticFiles(directory="static"), name="static")

app.include_router(panel.router, prefix="/panel", tags=["panel"])