from app.db import supabase
from openai import AsyncOpenAI, OpenAIError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI()

async def generate_summary(session_id: str):
    events = supabase.table("session_events") \
        .select("content, created_at") \
        .eq("session_id", session_id) \
        .order("created_at") \
        .execute()

    if not events.data:
        return

    conversation = "\n".join(event["content"] for event in events.data)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a concise summary of the following conversation."
                },
                {
                    "role": "user",
                    "content": conversation
                }
            ]
        )
        summary_text = response.choices[0].message.content

    except OpenAIError:
        summary_text = (
            "[LLM unavailable] Summary could not be generated due to API quota limits."
        )

    start_time = events.data[0]["created_at"]
    end_time = datetime.utcnow()
    duration = int((end_time - start_time).total_seconds())

    supabase.table("sessions").update({
        "summary": summary_text,
        "end_time": end_time,
        "duration_seconds": duration
    }).eq("session_id", session_id).execute()
