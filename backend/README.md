# 🧠 Chatbot Suite (Backend)

FastAPI + GPT‑4o‑mini backend with MongoDB ("mango") message history.  
Everything runs inside Docker — no manual DB setup required.

> **Status:** ✅ Backend complete · Connected to frontend

---

## ✅ What It Does

- Accepts `POST /api/chatbot/chat` requests
- Sends user query + history to GPT‑4o‑mini (via OpenRouter)
- Tracks sessions via a browser cookie (`session_id`)
- Stores all chats in MongoDB (`chatbot_db.chats`)

---

## 🗂️ Backend Structure

```
backend/
├─ app/
│  ├─ api/              # Routes → chatbot.py is the main endpoint
│  ├─ core/             # config.py (.env loader) + logger.py
│  ├─ db/               # crud.py (Mongo ops) + mango.py (connect)
│  ├─ schemas/          # Pydantic models
│  ├─ services/         # openrouter_client.py (GPT call)
│  └─ main.py           # FastAPI app entrypoint
├─ log/
│  └─ app.log           # App logs saved here
├─ .env                 # Secrets / config (excluded from Git)
├─ Dockerfile           # Backend container build
├─ requirements.txt     # Python dependencies
```

---

## 🍋 What is `mango.py`?

`mango.py` handles MongoDB connection using the `motor` async driver.

```python
# backend/app/db/mango.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_mango_uri

client = AsyncIOMotorClient(get_mango_uri())
db = client["chatbot_db"]
```

- Connects to `MONGO_URI` from `.env`
- Uses `chatbot_db` as the database
- Collection `chats` stores each user's message history

---

## ⚙️ .env Configuration (in `backend/`)

```env
MONGO_URI=mongodb://mongo:27017
OPENROUTER_API_KEY=your_openrouter_api_key
```

> 🔁 Use `mongo` as the hostname — it refers to the MongoDB Docker service, not `localhost`.
> You’ll get your OpenRouter key from https://openrouter.ai/docs/api-reference/authentication

---

## 🐳 Docker Compose Setup

All services (backend, MongoDB, frontend) are containerized:

```yaml
version: "3.9"

services:
  mongo:
    image: mongo:6
    container_name: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

  backend:
    build: ./backend
    working_dir: /app
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 7000
    ports:
      - "7000:7000"
    environment:
      - PYTHONUNBUFFERED=1
    develop:
      watch:
        - action: sync
          path: ./backend
          target: /app
          ignore:
            - __pycache__/
            - "*.pyc"

volumes:
  mongo-data:
```

---

## ▶️ Run Backend (with MongoDB and Frontend)

From project root (where `docker-compose.yml` is):

```bash
docker compose up --build
```

Then visit:

- Backend: [http://localhost:7000](http://localhost:7000)
- Chat API: `POST /api/chatbot/chat`

---

## 💾 MongoDB Schema (`chatbot_db.chats`)

Each chat session is stored as:

```json
{
  "session_id": "uuid-string",
  "messages": [
    { "role": "system",    "content": "..." },
    { "role": "user",      "content": "..." },
    { "role": "assistant", "content": "..." }
  ],
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

---

## 🔍 MongoDB Access & Debugging

### ⛏️ Open Mongo Shell

```bash
docker exec -it mongo mongosh
```

Then run:

```javascript
use chatbot_db
db.chats.find().pretty()
```

### 📦 View Data Volume

```bash
docker volume ls
docker volume inspect chatbot-suite_mongo-data
```

To delete old volume:

```bash
docker volume rm chatbot-suite_mongo-data
```

### 🧭 MongoDB Compass Access

Connect to:

```
mongodb://localhost:27017
```

Database name: `chatbot_db`

---

## 🛠️ Developer Notes

- `chatbot.py`:  
  - Reads session cookie  
  - Loads chat history  
  - Sends it to GPT‑4o‑mini via OpenRouter  
  - Saves new reply into MongoDB

- `crud.py`:  
  - Uses `update_one()` with `$set` and `$setOnInsert`

- `mango.py`:  
  - MongoDB client using `motor`

- `log/app.log`:  
  - All logs are saved here for debugging

---
