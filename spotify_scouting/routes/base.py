
from time import time
from typing import Annotated, Dict, Optional
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Cookie, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from models.models import SubmitRequest
from service.spotify import spotify_handler
from models.errors import NotSignedIn


base = APIRouter(
    prefix="",
    tags=["base"]
)

@base.get("/", response_class=HTMLResponse)
def main_page(response : Response, user_token: Annotated[Optional[str], Cookie()] = None):
    if user_token is None:
        response.set_cookie(key="user_token", value=str(uuid4()).split("-")[-1])
    with open(Path("spotify_scouting/web_pages/index.html")) as f:
        return f.read()
    
@base.post("/submit")
def submit(body: Dict, user_token: Annotated[Optional[str], Cookie()] = None):
    params = SubmitRequest(**body)
    try:
        sv = spotify_handler.get_instance(token=user_token)
    except NotSignedIn:
        return Response(content="Not signed in", status_code=500)
    sv.submit_playlist(params)
    return "we have submitted the playlist"

@base.get("/jobs")
def jobs():
    # if int(time()) % 2:
    #     return []
    return [
        {
            "id": "job-123",
            "name": "some playlist",
            "status": "running"
        },
        {
            "id": "job-456",
            "name": "another playlist",
            "status": "completed"
        }
    ]

@base.get("/check-signed-in")
def check_signed_in(user_token: Annotated[Optional[str], Cookie()] = None):
    if user_token in spotify_handler.instances:
        return 1
    else:
        return 0

@base.get("/sign-in", response_class=RedirectResponse)
def spot(user_token: Annotated[Optional[str], Cookie()] = None):
    sv = spotify_handler.create_instance(None)
    return sv.auth.get_authorize_url()

@base.get("/callback")
def auth_cb(request: Request, user_token: Annotated[Optional[str], Cookie()] = None):
    sv = spotify_handler.create_instance(token=user_token)
    sv.auth.process_auth_response(str(request.url))
    html_body = """
        <html>
            <head>
                <script type="text/javascript">
                    window.close();
                </script>
            </head>
            <body>
                <p>Operation succcessful. You can safely close this window.</p>
            </body>
        </html>

    """

    return Response(
        status_code=200,
        content=html_body,
        headers={
            'Content-Type': 'text/html'
        }
    )

@base.get("/cookie")
def get_token(user_token: Annotated[Optional[str], Cookie()] = None):
    return {"user_token": user_token}


@base.post("/cookie")
def set_token(response: Response):

    return