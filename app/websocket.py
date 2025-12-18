from fastapi import WebSocket
from app.db import supabase
from app.llm import stream_llm

async def session_ws(websocket: WebSocket, session_id: str):
    await websocket.accept()

    supabase.table("sessions").insert({
        "session_id": session_id,
        "user_id": "demo_user"
    }).execute()

    messages = [{"role": "system", "content": "You are a helpful assistant"}]

    try:
        while True:
            user_msg = await websocket.receive_text()

            supabase.table("session_events").insert({
                "session_id": session_id,
                "event_type": "user",
                "content": user_msg
            }).execute()

            messages.append({"role": "user", "content": user_msg})

            assistant_reply = ""

            async for event in stream_llm(messages):
                if event["type"] == "token":
                    assistant_reply += event["content"]
                    await websocket.send_text(event["content"])

            # Save assistant response
            messages.append({"role": "assistant", "content": assistant_reply})

            supabase.table("session_events").insert({
                "session_id": session_id,
                "event_type": "assistant",
                "content": assistant_reply
            }).execute()

    except Exception as e:
        print("WebSocket closed:", e)
