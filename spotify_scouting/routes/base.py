
from time import time
from typing import Dict

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from spotify_scouting.models.models import SubmitRequest


base = APIRouter(
    prefix="",
    tags=["base"]
)


@base.get("/", response_class=HTMLResponse)
def main_page():
    with open(r"web_pages\index.html") as f:
        return f.read()
    
@base.post("/submit")
def submit(body: Dict):
    print(body)
    params = SubmitRequest(**body)
    print(params)
    return "we have submitted the playlist"


@base.get("/jobs")
def jobs():
    if int(time()) % 2:
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
    return []