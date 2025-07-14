# 🧠 Chatbot Suite – Fullstack AI Chatbot
A fullstack chatbot built with:

- 🔙 **Backend**: FastAPI + OpenRouter (GPT-4o-mini)
- ⚛️ **Frontend**: React + Vite + Tailwind CSS
- 🛢️ **Database**: MongoDB (Dockerized)
- 🐳 **Deployment**: Docker Compose (full watch mode support)

## 🚀 Features

- Ask anything → get AI-powered responses via OpenRouter
- Conversations are saved with session-based history (using cookies)
- MongoDB stores chat messages
- Fully containerized (Docker Compose)

---

## 📁 Project Structure

```
chatbot-suite/
├── backend/
│   ├── app/              # FastAPI code
│   ├── .env              # API keys and Mongo URI
│   ├── Dockerfile        # Backend image
│   └── requirements.txt  # Python deps
├── frontend/
│   ├── src/              # React + Tailwind UI
│   ├── Dockerfile        # Frontend image
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml    # Multi-service definition
└── README.md             # You are here
```

## 🔗 How Frontend Talks to Backend

- Frontend runs on `http://localhost:5173`
- It sends `POST` requests to `http://localhost:7000/api/chatbot/chat`
- Requests include cookies for session tracking (`credentials: include`)
- Backend responds with updated messages and stores them in MongoDB : `mongodb://mongo:27017`

---

## 🐋 Run the Fullstack App with Docker Compose

Make sure Docker and Docker Compose are installed.

### 1. Clone and Navigate

```bash
git clone https://github.com/PawanYN/chatbot-suite.git
cd chatbot-suite
```
### 2. Add `.env` in Backend

Create `backend/.env`:

```
OPENROUTER_API_KEY=your_api_key_here
MONGO_URI=mongodb://mongo:27017
```
> You’ll get your OpenRouter key from https://openrouter.ai/docs/api-reference/authentication

### 3. Start All Services

```bash
docker compose up --build
```

Services started:

- 🔁 `http://localhost:5173` → Frontend (Vite Dev Server)
- 🧠 `http://localhost:7000` → FastAPI backend
- 📦 MongoDB → running in Docker at `localhost:27017`

---

## 📡 API: Chat Endpoint

### POST `/api/chatbot/chat`

Frontend and curl/postman clients can hit:

```
POST http://localhost:7000/api/chatbot/chat
```

**Request JSON**:

```json
{ "query": "Who is Krishna?" }
```

**Response JSON**:

```json
{
  "reply": "Krishna is the Supreme Personality of Godhead...",
  "session_id": "uuid...",
  "update": {
    "matched_count": 1,
    "modified_count": 1,
    "upserted_id": null
  }
}
```

---

## 🧠 MongoDB Schema (Collection: `chats`)

```json
{
  "session_id": "uuid",
  "messages": [
    { "role": "system", "content": "..." },
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "..." }
  ],
  "created_at": "...",
  "updated_at": "..."
}
```
View in shell:

```bash
docker exec -it mongo mongosh
use chatbot_db
db.chats.find().pretty()
```

## 🛠️ Dev Workflow (Live Reloading)

Thanks to Docker Compose's `develop.watch`, your code changes reflect instantly:

- 🔄 Backend auto-reloads via `uvicorn --reload`
- 🔄 Frontend hot-reloads via Vite (`npm run dev`)

---


## 📦 Docker Compose (Simplified View)

```yaml
version: "3.9"
services:
  mongo:
    image: mongo:6
    ports: ["27017:27017"]
    volumes: [mongo-data:/data/db]

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    ports: ["5173:5173"]
    develop:
      watch:
        - action: sync
          path: ./frontend
          target: /app
          ignore: [node_modules/]

  backend:
    build: ./backend
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 7000
    ports: ["7000:7000"]
    develop:
      watch:
        - action: sync
          path: ./backend
          target: /app
          ignore: [__pycache__/, "*.pyc"]
volumes:
  mongo-data:
```
---

## 🧪 Test Locally (Optional)

```bash
curl -X POST http://localhost:7000/api/chatbot/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "Explain dharma in short"}'
```

---

## ✅ Future Roadmap

- [x] Fullstack containerization
- [x] MongoDB history with `session_id`
- [ ] User authentication
- [ ] Chat UI improvements