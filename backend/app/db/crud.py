from app.core.logger import logger
logger.info("db/crud enter")
from app.db.mango import db
from app.schemas.chatbot import Createchat

from datetime import datetime, timezone
from uuid import uuid4
from bson import ObjectId
from fastapi import HTTPException
from bson import json_util  
import json


async def get_chat_by_session(session_id: str):
    """
    Return the chat document for `session_id` or raise 404.
    """
    if not session_id:
        logger.warning("get_chat_by_session called with empty session_id")
        raise HTTPException(status_code=400, detail="Session ID missing")

    chat = await db.chats.find_one({"session_id": session_id})

    if chat is None:
        logger.info(f"No chat found for session_id={session_id!r}")
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_pretty = json.dumps(chat, default=json_util.default, indent=2)
    logger.debug("Chat document for %s:\n%s", session_id, chat_pretty)
    return chat


async def update_chat( chat: Createchat):
    
    logger.info("I enter the update messages")
    
    now = datetime.now(timezone.utc)

    # ------------------------------------------------------------------ #
    #  Build the upsert
    #    - filter  : match by session_id only
    #    - $set    : always overwrite messages + updated_at
    #    - $setOnInsert : created_at only on first insert
    # ------------------------------------------------------------------ #
    filter_ = {"session_id": chat.session_id}

    update_ops = {
        "$set": {
            "messages":   chat.messages,
            "updated_at": now,
        },
        "$setOnInsert": {
            "created_at": now,
        },
    }
    try:
        result =await db.chats.update_one(filter_, update_ops, upsert=True)
        logger.info(f"Chat upserted for session_id={chat.session_id}")
        return {
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None
         }
    except Exception:
        logger.exception("Failed to upsert chat")
        return None
    
    
logger.info("db/crud out")