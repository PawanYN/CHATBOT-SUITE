from app.core.logger import logger
logger.info("main enter")
from app.api import chatbot

from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Chatbot API",   
    version="1.0.0",
    description="Backend API for chatbot app",
)

# ───────────────────────
# CORS — allow frontend access (React etc.)
# ───────────────────────
origins = [
    "http://localhost:3000",  # frontend dev
    "http://127.0.0.1:3000",
    # add prod domain here if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ───────────────────────
# Routers
# ───────────────────────
@app.get("/")
async def root():
    return {"msg": "Welcome to the Chatbot API"}

app.include_router(chatbot.router, prefix="/api")
# app.include_router(user.router, prefix="/api")



# ───────────────────────
# Startup / shutdown logs
# ───────────────────────
@app.on_event("startup")
async def on_startup():
    logger.info("🚀 Chatbot API server starting up...")
  
@app.on_event("shutdown")
async def on_shutdown():
    logger.info("🛑 Chatbot API server shutting down...")
    
logger.info("main out") 