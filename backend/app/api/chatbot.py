from app.core.logger import logger
logger.info("api/chatbot enter")
from app.services.openrouter_client import assistant
import app.core.config
from app.schemas.chatbot import Createchat
from app.db.crud import update_chat,get_chat_by_session
from app.db.mango import db


from fastapi import APIRouter, Request, Response, HTTPException
from uuid import uuid4

# import asyncio



#----------------------1.  router --------------------
SESSION_COOKIE = "session_id"


router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],         
)

#--------------------2. chatbot routes -------------------------------------------------


@router.get("/")
async def chatbot():
      return "Here, I am to help you out by answering your questions"
    
@router.post("/chat")
async def chat(query:str,request: Request, response: Response):

    logger.info("api/chatbot Post /chat entered")
    
    # 1. Get Session_id from cookie
    session_id=request.cookies.get(SESSION_COOKIE)
    print(session_id)
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(
            key=SESSION_COOKIE,
            value=session_id,
            httponly=True,
            samesite="lax",
            secure=False,   # switch to True on HTTPS
            path="/"
        )
          
          
    # 2. Load existing chat if any
    try:
        chat =await get_chat_by_session(session_id)
        messages=chat["messages"]
    except Exception as e:
        logger.warning("Falling back to new chat: %s", e)
        messages = [
            {"role": "system", "content": app.core.config.default_model.system_content},
        ]
  
    # 3. Add user query to messages
    messages.append({"role": "user", "content": query})
    print(messages)
    # 4. Get assistant response
    logger.info("OpenRouter assistant starting")
    try:
        result = await assistant(messages)
        print(result)
    except Exception:
        logger.exception("Assistant Error")
        raise HTTPException(status_code=500,detail="AI failed")
    
    messages.append({"role": "assistant",  "content":result})
    
    
    # 5. Create chat object and update DB
    chat_data=Createchat(
        session_id=session_id,
        messages=messages
    )

    try:
        update=await update_chat(chat_data)
    except :
        logger.exception("Update chat failed")
        raise HTTPException(status_code=500, detail="DB write error")

    logger.info("api/chatbot POST /chat completed")
    
    return {
        "reply": result,
        "session_id": session_id,
        "update":update,
    }

        
logger.info("api/chatbot out")