# Realtime AI Backend (WebSockets + Supabase)

## Overview

This project implements a high-performance asynchronous backend for a real-time AI conversation session.  
It demonstrates:

- WebSocket-based real-time streaming
- LLM interaction with function/tool calling
- State management across multiple turns
- Persistent storage using Supabase (PostgreSQL)
- Post-session summary generation
- Graceful fallback if OpenAI quota is exceeded

> This project focuses on backend functionality. A minimal frontend is provided to test the WebSocket.

## Tech Stack

- **FastAPI** – Async backend framework
- **WebSockets** – Real-time bidirectional communication
- **OpenAI API** – LLM streaming & tool calling
- **Supabase (PostgreSQL)** – Persistent storage
- **Python 3.10+** or **VS Code**

---

## 1. Detailed Setup Steps and Required Dependencies

### 1. Clone the repository
```
git clone https://github.com/Shubkartik/realtime-ai-backend.git
```
```
cd realtime-ai-backend
```

### 2. Create a virtual environment
```
python -m venv venv
```

### 3. Activate virtual environment

Windows :
```
venv\Scripts\activate
```
Mac/Linux
```
source venv/bin/activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Configure environment variables
Create a .env file in the root of the project:
### .env
```
OPENAI_API_KEY=your_key_here

SUPABASE_URL=https://xxxx.supabase.co

SUPABASE_KEY=your_service_role_key
```

## 2. Supabase Database Schema

Run the following SQL in your Supabase SQL editor:
```
-- Main session table

CREATE TABLE sessions (
    session_id UUID PRIMARY KEY,
    user_id TEXT,
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP,
    duration_seconds INT,
    summary TEXT
);

-- Event log table

CREATE TABLE session_events (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id),
    event_type TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```
## 3. How to Run and Test the WebSocket Server

### 1. Start FastAPI server
```
uvicorn app.main:app --reload
```
Server will run at: http://127.0.0.1:8000

### 2. Open frontend for testing

- Open frontend/index.html in a browser.

- Click Start Session → generates a session ID and opens a WebSocket

- Type a message in the input field → click Send

- Messages from the LLM will stream in real-time

- When you close the tab, a session summary is automatically generated in Supabase

### 3. Test function/tool calling

Type a message like:   fetch internal user analytics

 Expected behavior:

- Tool call detected

- Tool executed internally

- Response injected back into conversation stream

## 4. Key Design Choices

- WebSockets: Provides low-latency streaming between frontend and backend

- State management: Message history maintained for multi-turn conversations

- Function/Tool calling: Demonstrates complex LLM workflows

- Supabase: Persistent storage for sessions and event logs

- Post-session processing: Generates a concise session summary on disconnect

- Graceful fallback: Handles OpenAI quota errors without crashing the server


## 5. requirements.txt
```
fastapi
uvicorn
python-dotenv
supabase
openai
websockets
```
## 6. .env.example
### Rename to .env and fill in your own keys
```
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_service_role_key
```
