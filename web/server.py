from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.state import STATE


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="NetShield IDS",
    version="2.0.0"
)

app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static"
)


@app.get(
    "/",
    response_class=HTMLResponse
)
def index():

    with open(
        BASE_DIR / "templates" / "index.html",
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()


@app.get("/api/stats")
def stats():

    return STATE.get_stats()


@app.get("/api/events")
def events():

    return [
        event.to_dict()
        for event in STATE.get_events()
    ]


@app.get("/api/risks")
def risks():

    with STATE.lock:

        return dict(
            STATE.risk_scores
        )