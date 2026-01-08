
from fastapi import FastAPI
from backend.state import BackendState

app = FastAPI(title="DDoS Live Attack Map API")

state = BackendState()


@app.on_event("startup")
def startup():
    state.load()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/events")
def get_events():
    return state.events


@app.get("/events/{source_ip}")
def get_events_for_ip(source_ip: str):
    return [
        e for e in state.events
        if e["source_ip"] == source_ip
    ]
