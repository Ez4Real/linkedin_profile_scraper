from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse

async def unauthorized_handler(request: Request, exc: HTTPException):
    if not request.url.path.startswith('/auth'):
        if exc.status_code == 401:
            request.session['error_message'] = 'Log in first to access the panel'
            return RedirectResponse(url='/auth/login', status_code=302)
        return exc