from fastapi import FastAPI, Request, responses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mount the "static" folder to serve static files like CSS and JS
app.mount("/static/", StaticFiles(directory="static"), name="static")

# Create a Jinja2Templates instance and point it to the "templates" directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})