from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

from backend.state import state

app = FastAPI()

# ----------------------------
# CORS (frontend access)
# ----------------------------
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

# ----------------------------
# REST endpoints
# ----------------------------
@app.get("/events")
def get_events():
    return state.events


@app.get("/stats")
def get_stats():
    return state.get_stats()


# ----------------------------
# WebSocket: live event stream
# ----------------------------
@app.websocket("/ws/events")
async def websocket_events(ws: WebSocket):
    await ws.accept()

    last_sent = 0

    try:
        while True:
            
            if last_sent < len(state.events):
                new_events = state.events[last_sent:]
                await ws.send_text(json.dumps(new_events))
                last_sent = len(state.events)

            await asyncio.sleep(1)
    except Exception:
        
        pass
