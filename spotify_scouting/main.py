from spotify_scouting.app import app
import uvicorn

uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=8000
)