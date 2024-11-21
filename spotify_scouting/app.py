from typing import Dict, Union

from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from spotify_scouting.models import SubmitRequest

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def main_page():
    with open(r"web_pages\index.html") as f:
        return f.read()


@app.post("/submit")
def submit(body: Dict):
    params = SubmitRequest(**body)
    print(params)
    return "we have submitted the playlist"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}