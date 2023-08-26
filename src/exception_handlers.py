from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse

async def unauthorized_handler(request: Request, exc: HTTPException):
    if not request.url.path.startswith('/auth'):
        if exc.status_code == 401:
            return RedirectResponse(url='/auth/login', status_code=302)
        return exc
