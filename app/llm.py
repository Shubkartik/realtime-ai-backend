from dotenv import load_dotenv
load_dotenv()

from openai import AsyncOpenAI, OpenAIError
import json
import asyncio

client = AsyncOpenAI()

# -----------------------
# Fake internal tool
# -----------------------
def fetch_internal_data(query: str) -> str:
    return f"[MOCK TOOL] Internal data fetched for: {query}"

# -----------------------
# Tool schema
# -----------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_internal_data",
            "description": "Fetch internal company data based on a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query to fetch data for"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# -----------------------
# Streaming LLM with tool + fallback
# -----------------------
async def stream_llm(messages):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            stream=True
        )

        tool_call_data = None

        async for chunk in response:
            delta = chunk.choices[0].delta

            if delta.tool_calls:
                tool_call_data = delta.tool_calls[0]

            if delta.content:
                yield {"type": "token", "content": delta.content}

        # Tool execution
        if tool_call_data:
            args = json.loads(tool_call_data.function.arguments)
            tool_result = fetch_internal_data(args["query"])

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_data.id,
                "content": tool_result
            })

            followup = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True
            )

            async for chunk in followup:
                if chunk.choices[0].delta.content:
                    yield {"type": "token", "content": chunk.choices[0].delta.content}

    except OpenAIError:
        # 🔥 Graceful fallback when quota is exceeded
        fallback = (
            "[LLM unavailable — quota exceeded]\n"
            "Simulated streaming response for demo purposes.\n"
        )

        for word in fallback.split():
            await asyncio.sleep(0.05)
            yield {"type": "token", "content": word + " "}
