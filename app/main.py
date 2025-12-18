from fastapi import FastAPI, WebSocket
from app.websocket import session_ws
from app.summary import generate_summary

app = FastAPI()

@app.websocket("/ws/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    try:
        await session_ws(websocket, session_id)
    finally:
        try:
            await generate_summary(session_id)
        except Exception as e:
            print("Summary generation failed:", e)
