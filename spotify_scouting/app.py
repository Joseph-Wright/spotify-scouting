from fastapi import FastAPI
from spotify_scouting.routes.base import base


app = FastAPI(
    debug=True,
    title="Spotify Scout",
)

app.include_router(base)
