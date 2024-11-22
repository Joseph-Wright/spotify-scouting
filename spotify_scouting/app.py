from fastapi import FastAPI
from routes.base import base


app = FastAPI(
    debug=True,
    title="Spotify Scout",
)

app.include_router(base)
