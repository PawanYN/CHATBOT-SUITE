# 🧠 Chatbot Suite (Backend Only)

FastAPI + GPT‑4o‑mini backend with MongoDB message history.  
MongoDB runs locally in Docker.

> **Status:** Backend working · Frontend placeholder

---

## ✅ What It Does

- `POST /chatbot/chat?query=...`  
  → Sends query + history to GPT‑4o‑mini via OpenRouter  
  → Stores / updates the chat in MongoDB  
  → Tracks each conversation using a `session_id` cookie

---

## 🗂️ Key Folders

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
├─ .env                 # Your secrets / config (excluded from git)
├─ requirements.txt     # Python dependencies
├─ run.bat              # One-click server launcher
docker-compose.yml      # MongoDB Docker container
frontend/               # (empty for now)
```

---

## 🐋 MongoDB in Docker

This project uses Docker to run MongoDB locally — no manual install needed.

### `docker-compose.yml`

```yaml
version: '3'
services:
  mongo:
    image: mongo
    container_name: chatbot_mongo
    ports:
      - "27017:27017"
    volumes:
      - ./mongo_data:/data/db
```

### Start MongoDB

```bash
docker-compose up -d
```

Mongo will be available at:

```
mongodb://localhost:27017
```

---

## ⚙️ `.env` File (place in `backend/`)

```env
MONGO_URI=mongodb://localhost:27017
OPENROUTER_API_KEY="<put your OpenRouter API KEY>"
```

---

## ▶️ Run the Backend

From the `backend/` directory:

```bash
run.bat
```

Or manually:

```bash
uvicorn app.main:app --reload
```

FastAPI will run at:

```
http://localhost:8000
```

---

## 🔁 Chat Endpoint

### URL

```
POST /chatbot/chat?query=Hello
```

### Test with curl

```bash
curl -X POST "http://localhost:8000/chatbot/chat?query=Hello"
```

### Example Response

```json
{
  "reply": "I'm a helpful assistant. How can I assist you today?",
  "update": {
    "matched_count": 1,
    "modified_count": 1,
    "upserted_id": null
  }
}
```

---

## 💾 MongoDB Schema (`chats` collection)

Each document looks like this:

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

## 🔍 View Data in MongoDB

```bash
docker exec -it chatbot_mongo mongosh
use chatbot
db.chats.find().pretty()
```

---

## 🛠️ Dev Notes

- `chatbot.py`  
  → Reads `session_id` from cookies  
  → Loads previous chat from MongoDB  
  → Sends full message history to OpenRouter  
  → Appends new assistant reply  
  → Calls `update_chat()` to upsert into MongoDB

- `crud.py`  
  → Uses `update_one` with `$set` (always overwrite) and `$setOnInsert` (only first insert)

- Logs are saved in `log/app.log`

---

## 🚧 Future Improvements

- [ ] Add basic frontend (React / Next.js)
- [ ] Clear/reset chat history per session
- [ ] Auth support (per-user chats)
