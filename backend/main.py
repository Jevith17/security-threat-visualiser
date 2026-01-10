
from fastapi import FastAPI
from backend.state import BackendState
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="DDoS Live Attack Map API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
